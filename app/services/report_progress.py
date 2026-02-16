"""
Monthly Progress Report Service
Generates comprehensive monthly progress reports
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Assessment, PeriodLog, MentalHealthLog
from app.services.health_score_engine import HealthScoreEngine
from datetime import datetime, timedelta
import calendar


class ProgressReportService:
    """Service for generating monthly progress reports"""
    
    @staticmethod
    def get_month_name(month: int, year: int) -> str:
        """Get month name"""
        return f"{calendar.month_name[month]} {year}"
    
    @staticmethod
    def analyze_health_score_trend(db: Session, user_id: str) -> Dict[str, float]:
        """Analyze health score trend over the month"""
        
        # Get health scores from different weeks
        now = datetime.now()
        
        scores = {}
        
        # Current score
        current_score = HealthScoreEngine.calculate_health_score(db, user_id)
        scores["current"] = current_score["health_score"]
        
        # Note: In a real implementation, you'd store historical health scores
        # For now, we'll return current score
        scores["trend"] = "stable"  # Would calculate based on historical data
        
        return scores
    
    @staticmethod
    def analyze_cycle_regularity(db: Session, user_id: str) -> Optional[str]:
        """Analyze cycle regularity changes"""
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        recent_logs = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id,
            PeriodLog.created_at >= thirty_days_ago
        ).count()
        
        if recent_logs == 0:
            return "No period data logged this month"
        elif recent_logs == 1:
            return "One period logged - continue tracking for trend analysis"
        else:
            return "Regular tracking maintained - good progress!"
    
    @staticmethod
    def analyze_stress_trend(db: Session, user_id: str) -> Optional[str]:
        """Analyze stress trend"""
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        logs = db.query(MentalHealthLog).filter(
            MentalHealthLog.user_id == user_id,
            MentalHealthLog.created_at >= thirty_days_ago
        ).order_by(MentalHealthLog.created_at).all()
        
        if not logs:
            return "No mental health data logged this month"
        
        if len(logs) < 3:
            return "Limited data - continue logging for better insights"
        
        # Split into halves
        mid = len(logs) // 2
        first_half = logs[:mid]
        second_half = logs[mid:]
        
        avg_first = sum(log.stress_level for log in first_half) / len(first_half)
        avg_second = sum(log.stress_level for log in second_half) / len(second_half)
        
        diff = avg_second - avg_first
        
        if diff < -1:
            return "Stress levels decreased - excellent progress!"
        elif diff > 1:
            return "Stress levels increased - focus on stress management"
        else:
            return "Stress levels stable"
    
    @staticmethod
    def analyze_weight_trend(db: Session, user_id: str) -> Optional[str]:
        """Analyze weight trend"""
        
        # Get assessments from last 60 days
        sixty_days_ago = datetime.now() - timedelta(days=60)
        
        assessments = db.query(Assessment).filter(
            Assessment.user_id == user_id,
            Assessment.created_at >= sixty_days_ago
        ).order_by(Assessment.created_at).all()
        
        if len(assessments) < 2:
            return "Not enough data to track weight trend"
        
        first_weight = assessments[0].weight_kg
        last_weight = assessments[-1].weight_kg
        
        diff = last_weight - first_weight
        
        if abs(diff) < 1:
            return "Weight stable"
        elif diff < 0:
            return f"Weight decreased by {abs(diff):.1f} kg"
        else:
            return f"Weight increased by {diff:.1f} kg"
    
    @staticmethod
    def generate_key_achievements(db: Session, user_id: str) -> List[str]:
        """Generate list of key achievements"""
        
        achievements = []
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # Check period tracking
        period_count = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id,
            PeriodLog.created_at >= thirty_days_ago
        ).count()
        
        if period_count > 0:
            achievements.append(f"Logged {period_count} period entries this month")
        
        # Check mental health tracking
        mh_count = db.query(MentalHealthLog).filter(
            MentalHealthLog.user_id == user_id,
            MentalHealthLog.created_at >= thirty_days_ago
        ).count()
        
        if mh_count >= 20:
            achievements.append("Consistently tracked mental health (20+ entries)")
        elif mh_count >= 10:
            achievements.append("Good mental health tracking (10+ entries)")
        
        # Check health score
        health_score = HealthScoreEngine.calculate_health_score(db, user_id)
        if health_score["health_score"] >= 70:
            achievements.append(f"Maintained good health score: {health_score['health_score']}/100")
        
        if not achievements:
            achievements.append("Started your health tracking journey")
        
        return achievements
    
    @staticmethod
    def generate_recommendations(db: Session, user_id: str) -> List[str]:
        """Generate personalized recommendations"""
        
        recommendations = []
        
        # Get health score
        health_score = HealthScoreEngine.calculate_health_score(db, user_id)
        
        if health_score["health_score"] < 60:
            recommendations.append("Focus on improving your health score through better sleep and stress management")
        
        # Check period tracking
        thirty_days_ago = datetime.now() - timedelta(days=30)
        period_count = db.query(PeriodLog).filter(
            PeriodLog.user_id == user_id,
            PeriodLog.created_at >= thirty_days_ago
        ).count()
        
        if period_count == 0:
            recommendations.append("Start tracking your periods for better cycle insights")
        
        # Check mental health tracking
        mh_count = db.query(MentalHealthLog).filter(
            MentalHealthLog.user_id == user_id,
            MentalHealthLog.created_at >= thirty_days_ago
        ).count()
        
        if mh_count < 10:
            recommendations.append("Log your mental health daily for better pattern recognition")
        
        # General recommendations
        recommendations.append("Continue your PCOS management journey with consistent tracking")
        recommendations.append("Consult with healthcare providers for personalized medical advice")
        
        return recommendations
    
    @staticmethod
    def generate_monthly_report(db: Session, user_id: str) -> Dict:
        """Generate comprehensive monthly progress report"""
        
        now = datetime.now()
        period = ProgressReportService.get_month_name(now.month, now.year)
        
        # Gather all metrics
        health_score_trend = ProgressReportService.analyze_health_score_trend(db, user_id)
        cycle_regularity = ProgressReportService.analyze_cycle_regularity(db, user_id)
        stress_trend = ProgressReportService.analyze_stress_trend(db, user_id)
        weight_trend = ProgressReportService.analyze_weight_trend(db, user_id)
        achievements = ProgressReportService.generate_key_achievements(db, user_id)
        recommendations = ProgressReportService.generate_recommendations(db, user_id)
        
        return {
            "user_id": user_id,
            "period": period,
            "health_score_trend": health_score_trend,
            "cycle_regularity_change": cycle_regularity,
            "stress_trend": stress_trend,
            "weight_trend": weight_trend,
            "symptom_reduction": None,  # Would require historical symptom tracking
            "key_achievements": achievements,
            "recommendations": recommendations
        }
