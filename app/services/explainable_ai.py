import numpy as np
from typing import Dict, List, Tuple
from app.services.feature_engineering import FeatureEngineer

class ExplainableAI:
    """SHAP-like feature attribution for explaining predictions"""
    
    FEATURE_DESCRIPTIONS = {
        'cycle_irregularity': 'Irregular cycles',
        'hyperandrogenism': 'High androgen symptoms',
        'metabolic_risk': 'Metabolic factors',
        'bmi': 'Body Mass Index',
        'ovulation_risk': 'Ovulation issues',
        'lifestyle_risk': 'Lifestyle factors',
        'family_history': 'Family history',
        'stress_level': 'Stress levels',
        'sleep_hours': 'Sleep patterns',
        'exercise_days_per_week': 'Physical activity'
    }
    
    @staticmethod
    def calculate_feature_importance(features: Dict[str, float], 
                                    risk_score: float,
                                    phenotype: str) -> List[Tuple[str, float]]:
        """
        Calculate feature importance using gradient-based attribution
        Returns list of (feature_name, importance_score) sorted by importance
        """
        # Define phenotype-specific feature weights
        phenotype_weights = {
            "Insulin-resistant PCOS": {
                'metabolic_risk': 0.3,
                'bmi': 0.25,
                'cycle_irregularity': 0.2,
                'ovulation_risk': 0.15,
                'lifestyle_risk': 0.1
            },
            "Inflammatory PCOS": {
                'hyperandrogenism': 0.35,
                'metabolic_risk': 0.25,
                'lifestyle_risk': 0.25,
                'cycle_irregularity': 0.15
            },
            "Adrenal PCOS": {
                'lifestyle_risk': 0.4,
                'cycle_irregularity': 0.3,
                'ovulation_risk': 0.2,
                'metabolic_risk': 0.1
            },
            "Post-Pill PCOS": {
                'cycle_irregularity': 0.5,
                'ovulation_risk': 0.3,
                'lifestyle_risk': 0.2
            }
        }
        
        # Get weights for current phenotype
        weights = phenotype_weights.get(phenotype, phenotype_weights["Insulin-resistant PCOS"])
        
        # Calculate importance scores
        importance_scores = {}
        for feature_name, weight in weights.items():
            if feature_name in features:
                # Importance = weight * feature_value * risk_score
                importance = weight * features[feature_name] * (risk_score / 100)
                importance_scores[feature_name] = importance
        
        # Add other relevant features
        for feature_name in ['bmi', 'family_history', 'cycles_completeness']:
            if feature_name in features and feature_name not in importance_scores:
                importance = features[feature_name] * (risk_score / 100) * 0.1
                importance_scores[feature_name] = importance
        
        # Sort by importance
        sorted_importance = sorted(
            importance_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Convert to human-readable format
        key_drivers = []
        for feature_name, score in sorted_importance[:5]:  # Top 5 drivers
            description = ExplainableAI.FEATURE_DESCRIPTIONS.get(
                feature_name,
                feature_name.replace('_', ' ').title()
            )
            key_drivers.append(description)
        
        return key_drivers
    
    @staticmethod
    def generate_explanation(features: Dict[str, float],
                            risk_level: str,
                            phenotype: str,
                            risk_score: float,
                            confidence: float) -> str:
        """
        Generate human-readable explanation of the assessment
        """
        explanations = []
        
        # Risk level explanation
        if risk_level == "High":
            explanations.append("Your assessment indicates a higher pattern of risk factors associated with hormonal imbalance.")
        elif risk_level == "Moderate":
            explanations.append("Your assessment shows moderate indicators that may be worth discussing with a healthcare provider.")
        else:
            explanations.append("Your assessment shows lower risk indicators, but monitoring is still recommended.")
        
        # Phenotype explanation
        phenotype_explanations = {
            "Insulin-resistant PCOS": "This is the most common type of PCOS. Your pattern suggests insulin resistance, where the body doesn't use insulin properly. This can lead to weight gain, irregular periods, and hormonal imbalance. Lifestyle changes focusing on diet and exercise are particularly effective for this type.",
            "Inflammatory PCOS": "Your pattern indicates inflammatory factors that may be contributing to hormonal symptoms. This type is often triggered by stress, poor diet, or gut health issues. Anti-inflammatory approaches can be very helpful.",
            "Adrenal PCOS": "Your pattern suggests that stress hormones (from the adrenal glands) are significantly impacting your hormonal health. High stress, anxiety, and sleep issues are key factors. Stress management is crucial for this type.",
            "Post-Pill PCOS": "Your pattern suggests symptoms that may be related to hormonal changes after stopping birth control. This is often temporary and can improve naturally over 3-6 months with proper support."
        }
        
        explanations.append(phenotype_explanations.get(phenotype, ""))
        
        # Key contributing factors
        if features['cycle_irregularity'] > 0.5:
            explanations.append("Irregular menstrual cycles are a significant contributing factor.")
        if features['hyperandrogenism'] > 0.4:
            explanations.append("Signs of elevated androgen levels are present.")
        if features['metabolic_risk'] > 0.5:
            explanations.append("Metabolic factors appear to be contributing to the pattern.")
        if features['lifestyle_risk'] > 0.6:
            explanations.append("Lifestyle factors, particularly stress and sleep, are notable contributors.")
        
        return " ".join(explanations)

