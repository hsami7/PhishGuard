from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str
    role: Optional[str] = "analyst"

class UserResponse(UserBase):
    id: int
    email: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class EmailAnalysisRequest(BaseModel):
    raw_email: str

class EmailAnalysisResponse(BaseModel):
    category: str                # "phishing" | "legitimate" | "spam_junk"
    score_level: str             # "Low" | "Medium" | "High"
    numeric_score: int           # 0-100
    justification: str           # pipe-delimited summary
    explanation: dict            # structured breakdown by detection type
    explanation_text: str        # human-readable paragraph
    headers: dict
    urls: list[str]

class AnalysisHistoryResponse(BaseModel):
    id: int
    user_id: int
    sender: str
    subject: str
    category: str
    score_level: str
    numeric_score: int
    created_at: datetime

    class Config:
        orm_mode = True
