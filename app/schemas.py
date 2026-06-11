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
    score_level: str
    numeric_score: int
    justification: str
    headers: dict
    urls: list[str]

class AnalysisHistoryResponse(BaseModel):
    id: int
    user_id: int
    sender: str
    subject: str
    score_level: str
    numeric_score: int
    created_at: datetime

    class Config:
        orm_mode = True
