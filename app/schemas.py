from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

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

