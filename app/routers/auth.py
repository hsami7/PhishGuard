from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from slowapi.util import get_remote_address
from slowapi import Limiter
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.security import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import grpc
import sys
import os
import logging

# Audit client — fire-and-forget, non-blocking
def _audit_log(event_type: str, username: str = "", details: str = "", ip: str = "unknown"):
    """Send audit event to AuditService. Never raises — best effort only."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'protos'))
        from protos import audit_pb2, audit_pb2_grpc
        with grpc.insecure_channel('localhost:50052', options=[('grpc.enable_retries', 0)]) as channel:
            stub = audit_pb2_grpc.AuditServiceStub(channel)
            stub.LogEvent(audit_pb2.AuditEvent(
                event_type=event_type,
                username=username,
                details=details[:500],
                ip_address=ip
            ), timeout=2)
    except Exception:
        pass  # Audit must never break the main flow


def get_client_ip(request: Request) -> str:
    """Extract client IP from request, respecting proxies."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

limiter = Limiter(key_func=get_remote_address)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        role=user_create.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New user registered: {new_user.username}")
    _audit_log("USER_REGISTERED", username=new_user.username,
               details=f"New user registered: {new_user.username}", ip=get_client_ip(request))
    return new_user

@router.post("/token", response_model=Token)
@limiter.limit("10/minute")
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        _audit_log("USER_LOGIN_FAILED", username=form_data.username,
                   details=f"Failed login attempt for: {form_data.username}", ip=get_client_ip(request))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.username)}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in: {user.username}")
    _audit_log("USER_LOGIN", username=str(user.username),
               details=f"Successful login: {user.username}", ip=get_client_ip(request))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
