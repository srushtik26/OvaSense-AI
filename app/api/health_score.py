"""
Health Score API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import HealthScoreResponse
from app.services.health_score_engine import HealthScoreEngine

router = APIRouter()


@router.get("/{user_id}", response_model=HealthScoreResponse)
async def get_health_score(user_id: str, db: Session = Depends(get_db)):
    """
    Get health score for a user
    
    Calculates a comprehensive health score (0-100) based on:
    - Cycle regularity (25%)
    - BMI (15%)
    - Stress level (15%)
    - Sleep hours (15%)
    - Exercise frequency (15%)
    - Symptom severity (15%)
    """
    try:
        result = HealthScoreEngine.calculate_health_score(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
