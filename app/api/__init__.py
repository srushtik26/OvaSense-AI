from fastapi import APIRouter
from app.api.assessments import router as assessments_router

router = APIRouter()
router.include_router(assessments_router, prefix="/assessments", tags=["assessments"])
