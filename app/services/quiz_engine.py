"""
Quiz Engine Service
Manages PCOS awareness quiz questions and scoring
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import QuizQuestion, QuizResult


class QuizEngineService:
    """Service for quiz management and scoring"""
    
    @staticmethod
    def get_quiz_questions(db: Session, limit: int = 10) -> List[QuizQuestion]:
        """Get quiz questions"""
        return db.query(QuizQuestion).limit(limit).all()
    
    @staticmethod
    def calculate_score(db: Session, answers: Dict[int, str]) -> Dict:
        """Calculate quiz score based on answers"""
        
        correct_count = 0
        total_questions = len(answers)
        
        for question_id, user_answer in answers.items():
            question = db.query(QuizQuestion).filter(
                QuizQuestion.id == question_id
            ).first()
            
            if question and question.correct_answer.lower() == user_answer.lower():
                correct_count += 1
        
        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        return {
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": round(percentage, 1)
        }
    
    @staticmethod
    def get_awareness_level(percentage: float) -> str:
        """Determine awareness level based on score"""
        if percentage >= 90:
            return "Expert"
        elif percentage >= 70:
            return "Advanced"
        elif percentage >= 50:
            return "Intermediate"
        else:
            return "Beginner"
    
    @staticmethod
    def get_health_tips(awareness_level: str, percentage: float) -> List[str]:
        """Get health tips based on awareness level"""
        
        tips = {
            "Expert": [
                "Excellent! You have a strong understanding of PCOS.",
                "Share your knowledge with others in the PCOS community.",
                "Stay updated with the latest PCOS research.",
                "Consider becoming a PCOS advocate."
            ],
            "Advanced": [
                "Great job! You have good knowledge about PCOS.",
                "Continue learning about PCOS management strategies.",
                "Explore advanced topics like fertility and PCOS.",
                "Help educate others about PCOS awareness."
            ],
            "Intermediate": [
                "Good effort! You have basic understanding of PCOS.",
                "Learn more about PCOS symptoms and management.",
                "Explore diet and lifestyle modifications for PCOS.",
                "Consult healthcare providers for personalized advice."
            ],
            "Beginner": [
                "Keep learning! PCOS awareness is important.",
                "Start with understanding PCOS basics and symptoms.",
                "Learn about the importance of early diagnosis.",
                "Explore our educational resources and articles.",
                "Don't hesitate to ask healthcare professionals questions."
            ]
        }
        
        return tips.get(awareness_level, tips["Beginner"])
    
    @staticmethod
    def submit_quiz(db: Session, user_id: str, answers: Dict[int, str]) -> Dict:
        """Submit quiz and save results"""
        
        # Calculate score
        score_data = QuizEngineService.calculate_score(db, answers)
        
        # Determine awareness level
        awareness_level = QuizEngineService.get_awareness_level(score_data["percentage"])
        
        # Get health tips
        health_tips = QuizEngineService.get_health_tips(awareness_level, score_data["percentage"])
        
        # Save result
        quiz_result = QuizResult(
            user_id=user_id,
            score=score_data["score"],
            total_questions=score_data["total_questions"]
        )
        db.add(quiz_result)
        db.commit()
        db.refresh(quiz_result)
        
        return {
            "score": score_data["score"],
            "total_questions": score_data["total_questions"],
            "percentage": score_data["percentage"],
            "awareness_level": awareness_level,
            "health_tips": health_tips,
            "quiz_id": quiz_result.id
        }
