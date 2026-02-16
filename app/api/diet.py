"""
Diet Plan API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DietPlanResponse
from app.services.diet_personalizer import DietPersonalizerService

router = APIRouter()


@router.get("/{user_id}", response_model=DietPlanResponse)
async def get_diet_plan(user_id: str, db: Session = Depends(get_db)):
    """
    Get personalized diet plan based on PCOS phenotype and BMI
    
    Returns:
    - Foods to eat
    - Foods to avoid
    - Weekly meal plan
    - Nutritional tips
    """
    try:
        diet_plan = DietPersonalizerService.generate_diet_plan(db, user_id)
        return diet_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
