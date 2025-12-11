"""Quiz-related data models."""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator


class QuizRequest(BaseModel):
    """Request model for quiz generation."""
    topic: str = Field(..., min_length=2, max_length=200, description="Quiz topic")
    num_questions: int = Field(..., ge=3, le=20, description="Number of questions to generate")
    
    @field_validator('topic')
    @classmethod
    def topic_not_empty(cls, v: str) -> str:
        """Validate topic is not just whitespace."""
        if not v.strip():
            raise ValueError('Topic cannot be empty or whitespace only')
        return v.strip()


class Option(BaseModel):
    """Answer option model."""
    id: str = Field(..., description="Option identifier (A/B/C/D)")
    text: str = Field(..., description="Option text")


class Question(BaseModel):
    """Question model."""
    question_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique question ID")
    text: str = Field(..., description="Question text")
    options: List[Option] = Field(..., min_length=4, max_length=4, description="Four answer options")
    correct_answer_id: str = Field(..., description="ID of the correct option")
    
    @field_validator('correct_answer_id')
    @classmethod
    def validate_correct_answer(cls, v: str, info) -> str:
        """Validate correct answer ID exists in options."""
        if 'options' in info.data:
            valid_ids = [opt.id for opt in info.data['options']]
            if v not in valid_ids:
                raise ValueError(f'correct_answer_id must be one of {valid_ids}')
        return v


class QuizResponse(BaseModel):
    """Response model for successful quiz generation."""
    quiz_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique quiz ID")
    topic: str = Field(..., description="Quiz topic")
    questions: List[Question] = Field(..., description="List of questions")
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Generation timestamp")
    warning: Optional[str] = Field(None, description="Warning message if applicable")
    requested_questions: Optional[int] = Field(None, description="Originally requested number of questions")
    generated_questions: Optional[int] = Field(None, description="Actually generated number of questions")


class AnswerSubmission(BaseModel):
    """User's answer to a single question."""
    question_id: str = Field(..., description="Question ID")
    selected_answer_id: str = Field(..., description="Selected answer option ID")


class SubmitRequest(BaseModel):
    """Request model for quiz submission."""
    quiz_id: str = Field(..., description="Quiz ID")
    answers: List[AnswerSubmission] = Field(..., description="List of user answers")


class QuizResult(BaseModel):
    """Result for a single question."""
    question_id: str
    question_text: str
    selected_answer_id: str
    selected_answer_text: str
    correct_answer_id: str
    correct_answer_text: str
    is_correct: bool


class ScoreSummary(BaseModel):
    """Score summary."""
    correct: int
    total: int
    percentage: float


class SubmitResponse(BaseModel):
    """Response model for quiz submission."""
    quiz_id: str
    score: ScoreSummary
    results: List[QuizResult]
    submitted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ErrorResponse(BaseModel):
    """Generic error response."""
    error: str
    message: str
    details: Optional[dict] = None
