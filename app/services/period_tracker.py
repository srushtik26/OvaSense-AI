"""
Period Tracker Service
Manages period logging, cycle analysis, and predictions
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import PeriodLog
from datetime import datetime, date, timedelta


class PeriodTrackerService:
    """Service for period tracking and predictions"""
    
    @staticmethod
    def add_period_log(db: Session, user_id: str, start_date: date, 
                       end_date: Optional[date], flow_type: str, 
                       pain_level: int, mood: str) -> PeriodLog:
        """Add a new period log entry"""
        log = PeriodLog(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            flow_type=flow_type,
            pain_level=pain_level,
            mood=mood
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_period_history(db: Session, user_id: str, limit: int = 12) -> List[PeriodLog]:
        """Get period history for a user"""
        return db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id
        ).order_by(PeriodLog.start_date.desc()).limit(limit).all()
    
    @staticmethod
    def calculate_average_cycle_length(db: Session, user_id: str) -> Optional[float]:
        """Calculate average cycle length from historical data"""
        logs = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id
        ).order_by(PeriodLog.start_date).all()
        
        if len(logs) < 2:
            return None
        
        cycle_lengths = []
        for i in range(len(logs) - 1):
            days_diff = (logs[i+1].start_date - logs[i].start_date).days
            if days_diff > 0:  # Valid cycle
                cycle_lengths.append(days_diff)
        
        if not cycle_lengths:
            return None
        
        return sum(cycle_lengths) / len(cycle_lengths)
    
    @staticmethod
    def calculate_cycle_stability_score(db: Session, user_id: str) -> Optional[float]:
        """Calculate cycle stability score (0-100)"""
        logs = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id
        ).order_by(PeriodLog.start_date).all()
        
        if len(logs) < 3:
            return None
        
        cycle_lengths = []
        for i in range(len(logs) - 1):
            days_diff = (logs[i+1].start_date - logs[i].start_date).days
            if days_diff > 0:
                cycle_lengths.append(days_diff)
        
        if len(cycle_lengths) < 2:
            return None
        
        # Calculate standard deviation
        avg_length = sum(cycle_lengths) / len(cycle_lengths)
        variance = sum((x - avg_length) ** 2 for x in cycle_lengths) / len(cycle_lengths)
        std_dev = variance ** 0.5
        
        # Convert to score (lower std_dev = higher score)
        if std_dev <= 2:
            return 100.0
        elif std_dev <= 5:
            return 80.0
        elif std_dev <= 7:
            return 60.0
        elif std_dev <= 10:
            return 40.0
        else:
            return max(0, 40 - (std_dev - 10) * 2)
    
    @staticmethod
    def predict_next_period(db: Session, user_id: str) -> Dict:
        """Predict next period date based on historical data"""
        logs = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id
        ).order_by(PeriodLog.start_date.desc()).all()
        
        if not logs:
            return {
                "next_period_date": None,
                "confidence": "No Data",
                "average_cycle_length": None,
                "message": "Please log at least one period to get predictions."
            }
        
        if len(logs) < 2:
            # Use typical cycle length (28 days)
            last_period = logs[0].start_date
            predicted_date = last_period + timedelta(days=28)
            return {
                "next_period_date": predicted_date,
                "confidence": "Low",
                "average_cycle_length": 28.0,
                "message": "Prediction based on typical 28-day cycle. Log more periods for better accuracy."
            }
        
        # Calculate average cycle length
        cycle_lengths = []
        for i in range(len(logs) - 1):
            days_diff = (logs[i].start_date - logs[i+1].start_date).days
            if days_diff > 0:
                cycle_lengths.append(days_diff)
        
        if not cycle_lengths:
            last_period = logs[0].start_date
            predicted_date = last_period + timedelta(days=28)
            return {
                "next_period_date": predicted_date,
                "confidence": "Low",
                "average_cycle_length": 28.0,
                "message": "Using default 28-day cycle."
            }
        
        avg_cycle = sum(cycle_lengths) / len(cycle_lengths)
        
        # Calculate standard deviation for confidence
        variance = sum((x - avg_cycle) ** 2 for x in cycle_lengths) / len(cycle_lengths)
        std_dev = variance ** 0.5
        
        # Determine confidence
        if std_dev <= 3:
            confidence = "High"
            message = "Your cycles are very regular. This prediction is highly accurate."
        elif std_dev <= 7:
            confidence = "Medium"
            message = "Your cycles show moderate regularity. Prediction may vary by a few days."
        else:
            confidence = "Low"
            message = "Your cycles are irregular. This is an approximate prediction."
        
        # Predict next period
        last_period = logs[0].start_date
        predicted_date = last_period + timedelta(days=int(avg_cycle))
        
        return {
            "next_period_date": predicted_date,
            "confidence": confidence,
            "average_cycle_length": round(avg_cycle, 1),
            "message": message
        }
