"""
Period Tracker API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    PeriodLogInput, 
    PeriodLogResponse, 
    PeriodHistoryResponse,
    PeriodPredictionResponse
)
from app.services.period_tracker import PeriodTrackerService

router = APIRouter()


@router.post("/add", response_model=PeriodLogResponse)
async def add_period_log(period_data: PeriodLogInput, db: Session = Depends(get_db)):
    """
    Add a new period log entry
    """
    try:
        log = PeriodTrackerService.add_period_log(
            db=db,
            user_id=period_data.user_id,
            start_date=period_data.start_date,
            end_date=period_data.end_date,
            flow_type=period_data.flow_type,
            pain_level=period_data.pain_level,
            mood=period_data.mood
        )
        return log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}", response_model=PeriodHistoryResponse)
async def get_period_history(user_id: str, db: Session = Depends(get_db)):
    """
    Get period history for a user
    """
    try:
        logs = PeriodTrackerService.get_period_history(db, user_id)
        avg_cycle = PeriodTrackerService.calculate_average_cycle_length(db, user_id)
        stability = PeriodTrackerService.calculate_cycle_stability_score(db, user_id)
        
        return {
            "logs": logs,
            "average_cycle_length": avg_cycle,
            "cycle_stability_score": stability
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prediction/{user_id}", response_model=PeriodPredictionResponse)
async def get_period_prediction(user_id: str, db: Session = Depends(get_db)):
    """
    Get next period prediction for a user
    """
    try:
        prediction = PeriodTrackerService.predict_next_period(db, user_id)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
