from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QuestionGenerateRequest(BaseModel):
    role: str
    interview_type: str = "mixed"
    total_questions: int = Field(default=5, ge=3, le=15)
    experience_level: str = "mid"


class QuestionItem(BaseModel):
    question: str
    type: str = "technical"
    difficulty: str = "medium"
    keywords: List[str] = []
    time_limit: int = 300


class QuestionGenerateResponse(BaseModel):
    questions: List[QuestionItem]
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class EvaluateAnswerRequest(BaseModel):
    question: str
    answer: str
    expected_keywords: List[str] = Field(default_factory=list)
    question_type: str = "technical"


class EvaluationResponse(BaseModel):
    technical_score: float = Field(ge=0, le=100)
    communication_score: float = Field(ge=0, le=100)
    feedback: str
    missing_points: List[str] = []
    keywords_found: List[str] = []
    evaluation_at: datetime = Field(default_factory=datetime.utcnow)


class TranscribeRequest(BaseModel):
    audio_data: str


class TranscribeResponse(BaseModel):
    text: str
    language: Optional[str] = None
    confidence: float = 0.0
