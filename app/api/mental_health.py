"""
Mental Health Tracker API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    MentalHealthLogInput,
    MentalHealthLogResponse,
    MentalHealthHistoryResponse,
    MentalHealthInsightsResponse
)
from app.services.mental_health_tracker import MentalHealthTrackerService

router = APIRouter()


@router.post("/add", response_model=MentalHealthLogResponse)
async def add_mental_health_log(log_data: MentalHealthLogInput, db: Session = Depends(get_db)):
    """
    Add a new mental health log entry
    """
    try:
        log = MentalHealthTrackerService.add_mental_health_log(
            db=db,
            user_id=log_data.user_id,
            stress_level=log_data.stress_level,
            mood_type=log_data.mood_type,
            sleep_hours=log_data.sleep_hours,
            energy_level=log_data.energy_level
        )
        return log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}", response_model=MentalHealthHistoryResponse)
async def get_mental_health_history(user_id: str, db: Session = Depends(get_db)):
    """
    Get mental health history for a user
    """
    try:
        logs = MentalHealthTrackerService.get_mental_health_history(db, user_id)
        averages = MentalHealthTrackerService.calculate_averages(db, user_id)
        
        return {
            "logs": logs,
            **averages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/{user_id}", response_model=MentalHealthInsightsResponse)
async def get_mental_health_insights(user_id: str, db: Session = Depends(get_db)):
    """
    Get personalized mental health insights
    """
    try:
        insights = MentalHealthTrackerService.generate_insights(db, user_id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
