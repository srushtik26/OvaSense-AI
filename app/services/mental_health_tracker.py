"""
Mental Health Tracker Service
Manages mental health logging and insights generation
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import MentalHealthLog, PeriodLog
from datetime import datetime, timedelta


class MentalHealthTrackerService:
    """Service for mental health tracking and insights"""
    
    @staticmethod
    def add_mental_health_log(db: Session, user_id: str, stress_level: int,
                              mood_type: str, sleep_hours: float, 
                              energy_level: int) -> MentalHealthLog:
        """Add a new mental health log entry"""
        log = MentalHealthLog(
            user_id=user_id,
            stress_level=stress_level,
            mood_type=mood_type,
            sleep_hours=sleep_hours,
            energy_level=energy_level
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_mental_health_history(db: Session, user_id: str, days: int = 30) -> List[MentalHealthLog]:
        """Get mental health history for a user"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return db.query(MentalHealthLog).filter(
            MentalHealthLog.user_id == user_id,
            MentalHealthLog.created_at >= cutoff_date
        ).order_by(MentalHealthLog.created_at.desc()).all()
    
    @staticmethod
    def calculate_averages(db: Session, user_id: str, days: int = 30) -> Dict:
        """Calculate average mental health metrics"""
        logs = MentalHealthTrackerService.get_mental_health_history(db, user_id, days)
        
        if not logs:
            return {
                "average_stress": None,
                "average_sleep": None,
                "average_energy": None
            }
        
        return {
            "average_stress": round(sum(log.stress_level for log in logs) / len(logs), 1),
            "average_sleep": round(sum(log.sleep_hours for log in logs) / len(logs), 1),
            "average_energy": round(sum(log.energy_level for log in logs) / len(logs), 1)
        }
    
    @staticmethod
    def analyze_stress_trend(db: Session, user_id: str) -> str:
        """Analyze stress trend over time"""
        # Get last 30 days
        recent_logs = MentalHealthTrackerService.get_mental_health_history(db, user_id, 30)
        
        if len(recent_logs) < 3:
            return "stable"
        
        # Split into two halves
        mid_point = len(recent_logs) // 2
        recent_half = recent_logs[:mid_point]
        older_half = recent_logs[mid_point:]
        
        recent_avg = sum(log.stress_level for log in recent_half) / len(recent_half)
        older_avg = sum(log.stress_level for log in older_half) / len(older_half)
        
        diff = recent_avg - older_avg
        
        if diff > 1.5:
            return "increasing"
        elif diff < -1.5:
            return "decreasing"
        else:
            return "stable"
    
    @staticmethod
    def analyze_sleep_quality(db: Session, user_id: str) -> str:
        """Analyze sleep quality"""
        averages = MentalHealthTrackerService.calculate_averages(db, user_id)
        
        if averages["average_sleep"] is None:
            return "unknown"
        
        avg_sleep = averages["average_sleep"]
        
        if 7 <= avg_sleep <= 9:
            return "excellent"
        elif 6 <= avg_sleep < 7 or 9 < avg_sleep <= 10:
            return "good"
        elif 5 <= avg_sleep < 6 or 10 < avg_sleep <= 11:
            return "fair"
        else:
            return "poor"
    
    @staticmethod
    def generate_insights(db: Session, user_id: str) -> Dict:
        """Generate personalized mental health insights"""
        logs = MentalHealthTrackerService.get_mental_health_history(db, user_id, 30)
        
        insights = []
        recommendations = []
        
        if not logs:
            return {
                "insights": ["Not enough data. Start logging your mental health to get insights."],
                "stress_trend": "unknown",
                "sleep_quality": "unknown",
                "recommendations": ["Log your stress, mood, sleep, and energy levels daily."]
            }
        
        # Calculate metrics
        averages = MentalHealthTrackerService.calculate_averages(db, user_id)
        stress_trend = MentalHealthTrackerService.analyze_stress_trend(db, user_id)
        sleep_quality = MentalHealthTrackerService.analyze_sleep_quality(db, user_id)
        
        # Stress insights
        if averages["average_stress"] and averages["average_stress"] > 7:
            insights.append(f"Your average stress level is {averages['average_stress']}/10, which is high.")
            recommendations.append("Practice stress-reduction techniques like meditation or yoga.")
        elif averages["average_stress"] and averages["average_stress"] < 4:
            insights.append(f"Great! Your stress levels are well-managed at {averages['average_stress']}/10.")
        
        # Sleep insights
        if sleep_quality == "poor":
            insights.append(f"You're averaging {averages['average_sleep']} hours of sleep, which is below optimal.")
            recommendations.append("Aim for 7-9 hours of sleep per night for better health.")
        elif sleep_quality == "excellent":
            insights.append(f"Excellent! You're getting {averages['average_sleep']} hours of sleep on average.")
        
        # Energy insights
        if averages["average_energy"] and averages["average_energy"] < 4:
            insights.append(f"Your energy levels are low at {averages['average_energy']}/10.")
            recommendations.append("Consider increasing physical activity and improving sleep quality.")
        
        # Stress trend insights
        if stress_trend == "increasing":
            insights.append("Your stress levels have been increasing recently.")
            recommendations.append("Identify stress triggers and develop coping strategies.")
        elif stress_trend == "decreasing":
            insights.append("Great progress! Your stress levels are decreasing.")
        
        # Check correlation with period cycle
        period_logs = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id
        ).order_by(PeriodLog.start_date.desc()).limit(3).all()
        
        if period_logs and len(logs) >= 7:
            # Check if high stress occurs before periods
            high_stress_dates = [log.created_at.date() for log in logs if log.stress_level >= 7]
            
            for period in period_logs:
                # Check 5 days before period
                period_window_start = period.start_date - timedelta(days=5)
                period_window_end = period.start_date
                
                stress_before_period = any(
                    period_window_start <= stress_date <= period_window_end 
                    for stress_date in high_stress_dates
                )
                
                if stress_before_period:
                    insights.append("High stress detected before irregular cycles. This is common with PCOS.")
                    recommendations.append("Track your cycle and manage stress during pre-menstrual phase.")
                    break
        
        if not insights:
            insights.append("Your mental health metrics are within normal range. Keep it up!")
        
        if not recommendations:
            recommendations.append("Continue your current healthy habits.")
        
        return {
            "insights": insights,
            "stress_trend": stress_trend,
            "sleep_quality": sleep_quality,
            "recommendations": recommendations
        }
