from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Personal details
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    family_history_pcos = Column(Boolean)
    
    # Menstrual health
    cycle_length_avg = Column(Float)
    cycles_last_12_months = Column(Integer)
    missed_period_frequency = Column(Integer)  # Number of missed periods in last year
    period_flow_type = Column(String)  # light, normal, heavy
    taken_birth_control_pills = Column(Boolean)  # Has taken birth control pills
    
    # Symptoms
    acne_severity = Column(Integer)  # 0-5
    facial_hair_growth = Column(Integer)  # 0-5
    hair_thinning = Column(Integer)  # 0-5
    dark_patches_skin = Column(Boolean)
    
    # Metabolic
    sudden_weight_gain = Column(Boolean)
    fatigue_level = Column(Integer)  # 0-5
    sugar_cravings = Column(Integer)  # 0-5
    
    # Lifestyle
    stress_level = Column(Integer)  # 0-10
    sleep_hours = Column(Float)
    exercise_days_per_week = Column(Integer)
    diet_type = Column(String)  # vegetarian, non-vegetarian, vegan, etc.
    
    # Results
    risk_level = Column(String)  # Low, Moderate, High
    phenotype = Column(String)
    confidence_score = Column(Float)  # 0-1
    risk_score = Column(Float)  # 0-100
    key_drivers = Column(JSON)  # List of strings
    feature_values = Column(JSON)  # Engineered features
    shap_values = Column(JSON)  # SHAP explanations
    
    # User identifier (optional, for tracking over time)
    user_id = Column(String, nullable=True)

