from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=128)
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
    raw_email: str = Field(..., max_length=50000, description="Raw .eml content, max 50KB")
    sender: Optional[str] = Field(None, max_length=500, description="Optional explicit sender override (e.g. 'Name <email@.com>'). If provided, used instead of parser-extracted From header.")

class EmailAnalysisResponse(BaseModel):
    category: str
    score_level: str
    numeric_score: int
    justification: str
    explanation: dict
    explanation_text: str
    headers: dict
    urls: list[str]
    resolved_sender: str = ""

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
