from fastapi import APIRouter, Depends, HTTPException, status
import grpc
import sys
import os
import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.schemas import EmailAnalysisRequest, EmailAnalysisResponse, AnalysisHistoryResponse
from app.models import User
from app.security import get_current_user
from protos import analyzer_pb2
from protos import analyzer_pb2_grpc
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analysis", tags=["analysis"])

from analysis.parser import parse_email

@router.post("/", response_model=EmailAnalysisResponse)
def analyze_email(request: EmailAnalysisRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        parsed = parse_email(request.raw_email)
        # Use explicit sender if provided, otherwise fall back to parser-extracted From header
        sender = request.sender.strip() if request.sender and request.sender.strip() else parsed["headers"].get("From", "")
        subject = parsed["headers"].get("Subject", "")
        text_content = parsed["body_text"]
        urls = parsed["urls"]

        logger.info(f"User '{current_user.username}' requested analysis for sender: {sender}")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = analyzer_pb2_grpc.AnalysisServiceStub(channel)

            grpc_req = analyzer_pb2.EmailRequest(
                sender=sender,
                subject=subject,
                text_content=text_content,
                urls=urls
            )

            response = stub.AnalyzeEmail(grpc_req, timeout=10)

            # Parse the structured explanation from JSON
            explanation = {}
            try:
                explanation = json.loads(response.explanation_json)
            except (json.JSONDecodeError, TypeError):
                explanation = {}

            history_record = models.AnalysisHistory(
                user_id=current_user.id,
                sender=sender,
                subject=subject,
                category=response.category,
                score_level=response.score_level,
                numeric_score=response.numeric_score
            )
            db.add(history_record)
            db.commit()

            return EmailAnalysisResponse(
                category=response.category,
                score_level=response.score_level,
                numeric_score=response.numeric_score,
                justification=response.justification,
                explanation=explanation,
                explanation_text=response.explanation_text,
                headers=parsed["headers"],
                urls=urls,
                resolved_sender=sender
            )
    except grpc.RpcError as e:
        logger.error(f"gRPC service unavailable: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analysis service is currently unavailable. Please try again later."
        )

@router.get("/history", response_model=List[AnalysisHistoryResponse])
def get_history(
    sender: Optional[str] = None,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(models.AnalysisHistory).filter(models.AnalysisHistory.user_id == current_user.id)
    if sender:
        query = query.filter(models.AnalysisHistory.sender.ilike(f"%{sender}%"))
    if category:
        query = query.filter(models.AnalysisHistory.category == category)
    if keyword:
        query = query.filter(
            models.AnalysisHistory.subject.ilike(f"%{keyword}%") |
            models.AnalysisHistory.sender.ilike(f"%{keyword}%")
        )
    records = query.order_by(models.AnalysisHistory.created_at.desc()).offset(skip).limit(limit).all()
    return records
