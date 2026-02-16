"""
Monthly Progress Report API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MonthlyProgressReport
from app.services.report_progress import ProgressReportService

router = APIRouter()


@router.get("/monthly/{user_id}", response_model=MonthlyProgressReport)
async def get_monthly_report(user_id: str, db: Session = Depends(get_db)):
    """
    Get comprehensive monthly progress report
    
    Includes:
    - Health score trend
    - Cycle regularity changes
    - Stress trend analysis
    - Weight trend
    - Key achievements
    - Personalized recommendations
    """
    try:
        report = ProgressReportService.generate_monthly_report(db, user_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
