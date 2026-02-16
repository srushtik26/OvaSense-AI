from fastapi import APIRouter
from app.api.assessments import router as assessments_router
from app.api.health_score import router as health_score_router
from app.api.period import router as period_router
from app.api.mental_health import router as mental_health_router
from app.api.diet import router as diet_router
from app.api.quiz import router as quiz_router
from app.api.reports import router as reports_router

router = APIRouter()

# Existing routes
router.include_router(assessments_router, prefix="/assessments", tags=["assessments"])

# New engagement platform routes
router.include_router(health_score_router, prefix="/health-score", tags=["health-score"])
router.include_router(period_router, prefix="/period", tags=["period-tracker"])
router.include_router(mental_health_router, prefix="/mental-health", tags=["mental-health"])
router.include_router(diet_router, prefix="/diet-plan", tags=["diet"])
router.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
router.include_router(reports_router, prefix="/report", tags=["reports"])
