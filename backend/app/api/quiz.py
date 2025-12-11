"""Quiz API endpoints."""
from fastapi import APIRouter, HTTPException, status
from typing import Dict
import uuid

from app.models.quiz import (
    QuizRequest, 
    QuizResponse, 
    SubmitRequest, 
    SubmitResponse,
    QuizResult,
    ScoreSummary,
    ErrorResponse
)
from app.agents.quiz_generator import quiz_agent
from app.utils.cache import cache_manager

router = APIRouter()

# Store active quizzes for submission validation
QUIZ_CACHE_TTL = 60 * 60  # 1 hour


@router.post("/quiz/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Generate a new quiz based on the topic and number of questions."""
    
    # Check cache for existing quiz
    cache_key = f"quiz:{request.topic}:{request.num_questions}"
    cached_quiz = cache_manager.get(cache_key)
    if cached_quiz:
        return cached_quiz
    
    try:
        # Run the agent pipeline
        result = await quiz_agent.generate_quiz(request.topic, request.num_questions)
        
        # Check for errors
        if result.get("errors"):
            error_msg = "; ".join(result["errors"])
            
            # Check if it's a "not found" error
            if "no wikipedia articles found" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "error": "topic_not_found",
                        "message": f"Could not find Wikipedia content for topic: {request.topic}",
                        "suggestions": []
                    }
                )
            
            # Check if it's insufficient content
            if "insufficient content" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "error": "insufficient_content",
                        "message": error_msg,
                    }
                )
            
            # Generic error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "generation_failed",
                    "message": error_msg,
                    "request_id": str(uuid.uuid4())
                }
            )
        
        # Get validated questions
        questions = result.get("validated_questions", [])
        
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "generation_failed",
                    "message": "No valid questions were generated",
                    "request_id": str(uuid.uuid4())
                }
            )
        
        # Create response
        quiz_id = str(uuid.uuid4())
        
        # Check if we generated fewer questions than requested
        warning = None
        if len(questions) < request.num_questions:
            warning = "insufficient_content"
        
        response = QuizResponse(
            quiz_id=quiz_id,
            topic=result.get("resolved_topic", request.topic),
            questions=questions,
            warning=warning,
            requested_questions=request.num_questions if warning else None,
            generated_questions=len(questions) if warning else None
        )
        
        # Cache the quiz for submission later
        quiz_data = {
            "quiz_id": quiz_id,
            "questions": questions,
            "topic": response.topic
        }
        cache_manager.set(f"quiz_data:{quiz_id}", quiz_data, QUIZ_CACHE_TTL)
        
        # Cache the response
        cache_manager.set(cache_key, response, 24 * 60 * 60)  # 24 hours
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "generation_failed",
                "message": str(e),
                "request_id": str(uuid.uuid4())
            }
        )


@router.post("/quiz/submit", response_model=SubmitResponse)
async def submit_quiz(request: SubmitRequest):
    """Submit quiz answers and get results."""
    
    # Retrieve quiz data from cache
    quiz_data = cache_manager.get(f"quiz_data:{request.quiz_id}")
    
    if not quiz_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "quiz_not_found",
                "message": f"Quiz {request.quiz_id} not found or has expired"
            }
        )
    
    questions = quiz_data["questions"]
    
    # Create a map of question_id to question
    question_map = {q.question_id: q for q in questions}
    
    # Calculate results
    results = []
    correct_count = 0
    
    for answer in request.answers:
        question = question_map.get(answer.question_id)
        
        if not question:
            continue
        
        # Find the selected and correct answer texts
        selected_option = next((opt for opt in question.options if opt.id == answer.selected_answer_id), None)
        correct_option = next((opt for opt in question.options if opt.id == question.correct_answer_id), None)
        
        is_correct = answer.selected_answer_id == question.correct_answer_id
        if is_correct:
            correct_count += 1
        
        results.append(QuizResult(
            question_id=question.question_id,
            question_text=question.text,
            selected_answer_id=answer.selected_answer_id,
            selected_answer_text=selected_option.text if selected_option else "Unknown",
            correct_answer_id=question.correct_answer_id,
            correct_answer_text=correct_option.text if correct_option else "Unknown",
            is_correct=is_correct
        ))
    
    total = len(results)
    percentage = (correct_count / total * 100) if total > 0 else 0
    
    return SubmitResponse(
        quiz_id=request.quiz_id,
        score=ScoreSummary(
            correct=correct_count,
            total=total,
            percentage=round(percentage, 2)
        ),
        results=results
    )
