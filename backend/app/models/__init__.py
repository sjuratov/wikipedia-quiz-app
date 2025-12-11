"""Data models for the application."""
from app.models.quiz import (
    QuizRequest,
    QuizResponse,
    Question,
    Option,
    SubmitRequest,
    SubmitResponse,
    QuizResult
)

__all__ = [
    "QuizRequest",
    "QuizResponse",
    "Question",
    "Option",
    "SubmitRequest",
    "SubmitResponse",
    "QuizResult"
]
