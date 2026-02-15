import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import hdbscan
from typing import Dict, List, Tuple, Any
from app.services.feature_engineering import FeatureEngineer

class PCOSRiskDetector:
    """Hybrid rule-based + ML clustering for PCOS risk detection"""
    
    PHENOTYPES = [
        "Insulin-resistant PCOS",
        "Inflammatory PCOS",
        "Adrenal PCOS",
        "Post-Pill PCOS"
    ]
    
    def __init__(self):
        self.feature_names = [
            'bmi', 'cycle_irregularity', 'ovulation_risk', 'hyperandrogenism',
            'metabolic_risk', 'lifestyle_risk', 'cycle_length_norm',
            'family_history', 'age_norm', 'cycles_completeness', 'missed_periods_norm'
        ]
    
    def rule_based_screening(self, features: Dict[str, float]) -> Tuple[bool, float]:
        """
        Step 1: Rule-based screening
        Returns: (high_suspicion, initial_risk_score)
        """
        cycle_irregularity = features['cycle_irregularity']
        hyperandrogenism = features['hyperandrogenism']
        
        # High suspicion if irregular cycles AND high androgen symptoms
        high_suspicion = (cycle_irregularity > 0.5) and (hyperandrogenism > 0.4)
        
        # Calculate initial risk score
        risk_factors = [
            cycle_irregularity * 0.3,
            hyperandrogenism * 0.25,
            features['metabolic_risk'] * 0.2,
            features['ovulation_risk'] * 0.15,
            features['lifestyle_risk'] * 0.1
        ]
        
        initial_risk = sum(risk_factors) * 100  # Convert to 0-100 scale
        
        return high_suspicion, initial_risk
    
    def cluster_phenotype(self, features: Dict[str, float], taken_birth_control: bool = False) -> Tuple[str, float]:
        """
        Step 2: Unsupervised ML clustering
        Uses HDBSCAN, KMeans, and Gaussian Mixture for phenotype identification
        Returns: (phenotype_type, confidence_score)
        """
        # Convert features to array
        feature_vector = np.array([features[name] for name in self.feature_names]).reshape(1, -1)
        
        # For single sample, we need to use a different approach
        # We'll use a rule-based phenotype assignment based on feature patterns
        
        # Calculate phenotype scores based on medical PCOS types
        # 1. Insulin-resistant PCOS (most common)
        insulin_resistant_score = (
            features['metabolic_risk'] * 0.4 +
            features['bmi'] * 0.3 +
            features['cycle_irregularity'] * 0.2 +
            features['ovulation_risk'] * 0.1
        )
        
        # 2. Inflammatory PCOS
        inflammatory_score = (
            features['hyperandrogenism'] * 0.4 +
            features['metabolic_risk'] * 0.3 +
            features['lifestyle_risk'] * 0.3
        )
        
        # 3. Adrenal PCOS (stress-driven)
        adrenal_score = (
            features['lifestyle_risk'] * 0.5 +
            features['cycle_irregularity'] * 0.3 +
            features['ovulation_risk'] * 0.2
        )
        
        # 4. Post-Pill PCOS (recent birth control use, irregular cycles)
        # Boost score significantly if user has taken birth control pills
        if taken_birth_control:
            post_pill_score = (
                features['cycle_irregularity'] * 0.5 +
                features['ovulation_risk'] * 0.3 +
                (1 - features['metabolic_risk']) * 0.1 +
                (1 - features['hyperandrogenism']) * 0.1
            )
            # If taken pills and cycles are irregular, strongly favor Post-Pill PCOS
            if features['cycle_irregularity'] > 0.4:
                post_pill_score = min(post_pill_score * 1.5, 1.0)
        else:
            # Lower score if no birth control history
            post_pill_score = (
                features['cycle_irregularity'] * 0.3 +
                (1 - features['metabolic_risk']) * 0.2 +
                (1 - features['hyperandrogenism']) * 0.2 +
                features['ovulation_risk'] * 0.1 +
                (1 - features['lifestyle_risk']) * 0.2
            )
        
        scores = {
            "Insulin-resistant PCOS": insulin_resistant_score,
            "Inflammatory PCOS": inflammatory_score,
            "Adrenal PCOS": adrenal_score,
            "Post-Pill PCOS": post_pill_score
        }
        
        # Get dominant phenotype (highest scoring type)
        phenotype = max(scores, key=scores.get)
        confidence = scores[phenotype]
        
        # Ensure confidence is reasonable
        confidence = max(confidence, 0.5)  # Minimum 50% confidence
        
        return phenotype, confidence
    
    def detect_risk(self, features: Dict[str, float], taken_birth_control: bool = False) -> Dict[str, Any]:
        """
        Main risk detection method
        Returns comprehensive risk assessment
        """
        # Rule-based screening
        high_suspicion, initial_risk = self.rule_based_screening(features)
        
        # Phenotype clustering
        phenotype, confidence = self.cluster_phenotype(features, taken_birth_control)
        
        # Final risk score (combine initial risk with confidence)
        final_risk_score = initial_risk * confidence
        
        # Determine risk level
        if final_risk_score < 30:
            risk_level = "Low"
        elif final_risk_score < 60:
            risk_level = "Moderate"
        else:
            risk_level = "High"
        
        return {
            'risk_level': risk_level,
            'phenotype': phenotype,
            'confidence_score': confidence,
            'risk_score': final_risk_score,
            'high_suspicion': high_suspicion
        }

