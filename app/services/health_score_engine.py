"""
Health Score Engine Service
Calculates a comprehensive health score (0-100) based on multiple factors
"""
from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models import Assessment, PeriodLog, MentalHealthLog
from datetime import datetime, timedelta


class HealthScoreEngine:
    """Calculate health score based on weighted factors"""
    
    # Weight distribution (must sum to 100%)
    WEIGHTS = {
        'cycle_regularity': 0.25,
        'bmi': 0.15,
        'stress': 0.15,
        'sleep': 0.15,
        'exercise': 0.15,
        'symptoms': 0.15
    }
    
    @staticmethod
    def calculate_bmi(height_cm: float, weight_kg: float) -> float:
        """Calculate BMI"""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    @staticmethod
    def score_cycle_regularity(db: Session, user_id: str) -> float:
        """Score cycle regularity (0-100) based on period logs"""
        # Get recent period logs (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        logs = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id,
            PeriodLog.created_at >= six_months_ago
        ).order_by(PeriodLog.start_date).all()
        
        if len(logs) < 2:
            # Not enough data, check assessment
            assessment = db.query(Assessment).filter(
                Assessment.user_id == user_id
            ).order_by(Assessment.created_at.desc()).first()
            
            if assessment:
                # Use cycles_last_12_months as indicator
                if assessment.cycles_last_12_months >= 11:
                    return 100.0
                elif assessment.cycles_last_12_months >= 9:
                    return 75.0
                elif assessment.cycles_last_12_months >= 6:
                    return 50.0
                else:
                    return 25.0
            return 50.0  # Default if no data
        
        # Calculate cycle lengths
        cycle_lengths = []
        for i in range(len(logs) - 1):
            days_diff = (logs[i+1].start_date - logs[i].start_date).days
            cycle_lengths.append(days_diff)
        
        if not cycle_lengths:
            return 50.0
        
        # Calculate standard deviation
        avg_length = sum(cycle_lengths) / len(cycle_lengths)
        variance = sum((x - avg_length) ** 2 for x in cycle_lengths) / len(cycle_lengths)
        std_dev = variance ** 0.5
        
        # Score based on regularity (lower std_dev = more regular)
        if std_dev <= 2:
            return 100.0
        elif std_dev <= 5:
            return 80.0
        elif std_dev <= 7:
            return 60.0
        elif std_dev <= 10:
            return 40.0
        else:
            return 20.0
    
    @staticmethod
    def score_bmi(bmi: float) -> float:
        """Score BMI (0-100)"""
        if 18.5 <= bmi <= 24.9:
            return 100.0
        elif 25 <= bmi <= 29.9 or 17 <= bmi < 18.5:
            return 70.0
        elif 30 <= bmi <= 34.9 or 16 <= bmi < 17:
            return 40.0
        else:
            return 20.0
    
    @staticmethod
    def score_stress(db: Session, user_id: str) -> float:
        """Score stress level (0-100) based on recent mental health logs"""
        # Get recent logs (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        logs = db.query(MentalHealthLog).filter(
            MentalHealthLog.user_id == user_id,
            MentalHealthLog.created_at >= thirty_days_ago
        ).all()
        
        if not logs:
            # Check assessment
            assessment = db.query(Assessment).filter(
                Assessment.user_id == user_id
            ).order_by(Assessment.created_at.desc()).first()
            
            if assessment:
                stress_level = assessment.stress_level
            else:
                return 50.0  # Default
        else:
            stress_level = sum(log.stress_level for log in logs) / len(logs)
        
        # Convert stress (1-10) to score (100-0)
        # Lower stress = higher score
        return max(0, 100 - (stress_level * 10))
    
    @staticmethod
    def score_sleep(db: Session, user_id: str) -> float:
        """Score sleep hours (0-100)"""
        # Get recent logs
        thirty_days_ago = datetime.now() - timedelta(days=30)
        logs = db.query(MentalHealthLog).filter(
            MentalHealthLog.user_id == user_id,
            MentalHealthLog.created_at >= thirty_days_ago
        ).all()
        
        if not logs:
            # Check assessment
            assessment = db.query(Assessment).filter(
                Assessment.user_id == user_id
            ).order_by(Assessment.created_at.desc()).first()
            
            if assessment:
                sleep_hours = assessment.sleep_hours
            else:
                return 50.0
        else:
            sleep_hours = sum(log.sleep_hours for log in logs) / len(logs)
        
        # Optimal sleep: 7-9 hours
        if 7 <= sleep_hours <= 9:
            return 100.0
        elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
            return 75.0
        elif 5 <= sleep_hours < 6 or 10 < sleep_hours <= 11:
            return 50.0
        else:
            return 25.0
    
    @staticmethod
    def score_exercise(db: Session, user_id: str) -> float:
        """Score exercise frequency (0-100)"""
        assessment = db.query(Assessment).filter(
            Assessment.user_id == user_id
        ).order_by(Assessment.created_at.desc()).first()
        
        if not assessment:
            return 50.0
        
        days = assessment.exercise_days_per_week
        
        # Optimal: 4-6 days per week
        if 4 <= days <= 6:
            return 100.0
        elif days == 3 or days == 7:
            return 80.0
        elif days == 2:
            return 60.0
        elif days == 1:
            return 40.0
        else:
            return 20.0
    
    @staticmethod
    def score_symptoms(db: Session, user_id: str) -> float:
        """Score based on symptom severity (0-100)"""
        assessment = db.query(Assessment).filter(
            Assessment.user_id == user_id
        ).order_by(Assessment.created_at.desc()).first()
        
        if not assessment:
            return 50.0
        
        # Sum up symptom scores (each 0-5)
        total_symptoms = (
            assessment.acne_severity +
            assessment.facial_hair_growth +
            assessment.hair_thinning +
            assessment.fatigue_level +
            assessment.sugar_cravings
        )
        
        # Max possible: 25, convert to 0-100 scale (inverted)
        symptom_percentage = (total_symptoms / 25) * 100
        return max(0, 100 - symptom_percentage)
    
    @classmethod
    def calculate_health_score(cls, db: Session, user_id: str) -> Dict:
        """Calculate overall health score with breakdown"""
        
        # Get latest assessment for BMI calculation
        assessment = db.query(Assessment).filter(
            Assessment.user_id == user_id
        ).order_by(Assessment.created_at.desc()).first()
        
        if not assessment:
            return {
                "health_score": 0,
                "status": "No Data",
                "message": "Please complete an assessment first to get your health score.",
                "breakdown": {}
            }
        
        # Calculate BMI
        bmi = cls.calculate_bmi(assessment.height_cm, assessment.weight_kg)
        
        # Calculate component scores
        scores = {
            'cycle_regularity': cls.score_cycle_regularity(db, user_id),
            'bmi': cls.score_bmi(bmi),
            'stress': cls.score_stress(db, user_id),
            'sleep': cls.score_sleep(db, user_id),
            'exercise': cls.score_exercise(db, user_id),
            'symptoms': cls.score_symptoms(db, user_id)
        }
        
        # Calculate weighted total
        total_score = sum(scores[key] * cls.WEIGHTS[key] for key in scores)
        total_score = round(total_score)
        
        # Determine status
        if total_score >= 80:
            status = "Excellent"
            message = "Great job! Keep maintaining your healthy lifestyle."
        elif total_score >= 65:
            status = "Good"
            message = "You're doing well! Small improvements in sleep and stress management can boost your score."
        elif total_score >= 50:
            status = "Moderate"
            message = "Improving sleep and reducing stress can increase your score significantly."
        else:
            status = "Needs Improvement"
            message = "Focus on regular exercise, better sleep, and stress management to improve your health."
        
        return {
            "health_score": total_score,
            "status": status,
            "message": message,
            "breakdown": {k: round(v, 1) for k, v in scores.items()}
        }
