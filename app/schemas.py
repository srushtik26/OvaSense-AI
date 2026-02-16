from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime, date

class AssessmentInput(BaseModel):
    # Personal details
    age: int = Field(..., ge=13, le=60, description="Age in years")
    height_cm: float = Field(..., gt=0, description="Height in centimeters")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    family_history_pcos: bool = Field(..., description="Family history of PCOS")
    
    # Menstrual health
    cycle_length_avg: float = Field(..., gt=0, description="Average cycle length in days")
    cycles_last_12_months: int = Field(..., ge=0, le=12, description="Number of cycles in last 12 months")
    missed_period_frequency: int = Field(..., ge=0, description="Number of missed periods in last year")
    period_flow_type: str = Field(..., description="Period flow type: light, normal, or heavy")
    taken_birth_control_pills: bool = Field(..., description="Has taken birth control pills")
    
    # Symptoms
    acne_severity: int = Field(..., ge=0, le=5, description="Acne severity (0-5)")
    facial_hair_growth: int = Field(..., ge=0, le=5, description="Facial hair growth (0-5)")
    hair_thinning: int = Field(..., ge=0, le=5, description="Hair thinning (0-5)")
    dark_patches_skin: bool = Field(..., description="Dark patches on skin")
    
    # Metabolic
    sudden_weight_gain: bool = Field(..., description="Sudden weight gain")
    fatigue_level: int = Field(..., ge=0, le=5, description="Fatigue level (0-5)")
    sugar_cravings: int = Field(..., ge=0, le=5, description="Sugar cravings (0-5)")
    
    # Lifestyle
    stress_level: int = Field(..., ge=0, le=10, description="Stress level (0-10)")
    sleep_hours: float = Field(..., ge=0, le=24, description="Average sleep hours per day")
    exercise_days_per_week: int = Field(..., ge=0, le=7, description="Exercise days per week")
    diet_type: str = Field(..., description="Diet type")
    
    user_id: Optional[str] = None
    
    @validator('period_flow_type')
    def validate_flow_type(cls, v):
        if v.lower() not in ['light', 'normal', 'heavy']:
            raise ValueError('period_flow_type must be light, normal, or heavy')
        return v.lower()

class AssessmentResult(BaseModel):
    id: int
    created_at: datetime
    risk_level: str
    phenotype: str
    confidence_score: float
    risk_score: float
    key_drivers: List[str]
    remedies: List[str]
    next_steps: List[str]
    disclaimer: str = "This is not a medical diagnosis. Please consult a doctor for confirmation."

class AssessmentResponse(BaseModel):
    risk_level: str
    phenotype: str
    confidence: str
    risk_score: float
    key_drivers: List[str]
    remedies: List[str]
    next_steps: List[str]
    disclaimer: str = "This is not a medical diagnosis. Please consult a doctor for confirmation."
    assessment_id: Optional[int] = None


# ===== HEALTH SCORE SCHEMAS =====
class HealthScoreResponse(BaseModel):
    health_score: int
    status: str  # Low, Moderate, Good, Excellent
    message: str
    breakdown: Dict[str, float]  # Component scores


# ===== PERIOD TRACKER SCHEMAS =====
class PeriodLogInput(BaseModel):
    user_id: str
    start_date: date
    end_date: Optional[date] = None
    flow_type: str = Field(..., description="light, normal, or heavy")
    pain_level: int = Field(..., ge=1, le=10)
    mood: str = Field(..., description="happy, sad, anxious, irritable, normal")
    
    @validator('flow_type')
    def validate_flow_type(cls, v):
        if v.lower() not in ['light', 'normal', 'heavy']:
            raise ValueError('flow_type must be light, normal, or heavy')
        return v.lower()

class PeriodLogResponse(BaseModel):
    id: int
    user_id: str
    start_date: date
    end_date: Optional[date]
    flow_type: str
    pain_level: int
    mood: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PeriodHistoryResponse(BaseModel):
    logs: List[PeriodLogResponse]
    average_cycle_length: Optional[float]
    cycle_stability_score: Optional[float]

class PeriodPredictionResponse(BaseModel):
    next_period_date: Optional[date]
    confidence: str
    average_cycle_length: Optional[float]
    message: str


# ===== MENTAL HEALTH SCHEMAS =====
class MentalHealthLogInput(BaseModel):
    user_id: str
    stress_level: int = Field(..., ge=1, le=10)
    mood_type: str = Field(..., description="happy, sad, anxious, irritable, calm, energetic")
    sleep_hours: float = Field(..., ge=0, le=24)
    energy_level: int = Field(..., ge=1, le=10)

class MentalHealthLogResponse(BaseModel):
    id: int
    user_id: str
    stress_level: int
    mood_type: str
    sleep_hours: float
    energy_level: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MentalHealthHistoryResponse(BaseModel):
    logs: List[MentalHealthLogResponse]
    average_stress: Optional[float]
    average_sleep: Optional[float]
    average_energy: Optional[float]

class MentalHealthInsightsResponse(BaseModel):
    insights: List[str]
    stress_trend: str  # increasing, decreasing, stable
    sleep_quality: str  # poor, fair, good, excellent
    recommendations: List[str]


# ===== DIET PLAN SCHEMAS =====
class DietPlanResponse(BaseModel):
    phenotype: str
    bmi_category: str
    foods_to_eat: List[str]
    foods_to_avoid: List[str]
    weekly_meal_plan: Dict[str, List[str]]
    nutritional_tips: List[str]


# ===== QUIZ SCHEMAS =====
class QuizQuestionResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    
    class Config:
        from_attributes = True

class QuizSubmission(BaseModel):
    user_id: str
    answers: Dict[int, str]  # question_id: answer

class QuizResultResponse(BaseModel):
    score: int
    total_questions: int
    percentage: float
    awareness_level: str  # Beginner, Intermediate, Advanced, Expert
    health_tips: List[str]
    quiz_id: int


# ===== PROGRESS REPORT SCHEMAS =====
class MonthlyProgressReport(BaseModel):
    user_id: str
    period: str  # e.g., "January 2026"
    health_score_trend: Dict[str, float]
    cycle_regularity_change: Optional[str]
    stress_trend: Optional[str]
    weight_trend: Optional[str]
    symptom_reduction: Optional[Dict[str, str]]
    key_achievements: List[str]
    recommendations: List[str]

