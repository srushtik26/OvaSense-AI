"""
PCOS Awareness Quiz API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import QuizQuestionResponse, QuizSubmission, QuizResultResponse
from app.services.quiz_engine import QuizEngineService

router = APIRouter()


@router.get("/questions", response_model=List[QuizQuestionResponse])
async def get_quiz_questions(db: Session = Depends(get_db)):
    """
    Get PCOS awareness quiz questions
    """
    try:
        questions = QuizEngineService.get_quiz_questions(db)
        
        # Remove correct_answer from response
        return [
            {
                "id": q.id,
                "question": q.question,
                "options": q.options
            }
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit", response_model=QuizResultResponse)
async def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    """
    Submit quiz answers and get results
    
    Returns:
    - Score
    - Awareness level
    - Personalized health tips
    """
    try:
        result = QuizEngineService.submit_quiz(
            db=db,
            user_id=submission.user_id,
            answers=submission.answers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
