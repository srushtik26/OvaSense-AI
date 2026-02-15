import numpy as np
import pandas as pd
from typing import Dict, Any

class FeatureEngineer:
    """Engineers medically meaningful features from raw input data"""
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> float:
        """Calculate Body Mass Index"""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    @staticmethod
    def calculate_cycle_irregularity_index(cycle_length_avg: float, cycles_last_12_months: int, 
                                          missed_period_frequency: int) -> float:
        """
        Calculate cycle irregularity index (0-1)
        Higher value = more irregular
        """
        # Normal cycle is 21-35 days
        cycle_deviation = abs(cycle_length_avg - 28) / 28  # Deviation from 28-day average
        
        # Missing cycles
        expected_cycles = 12
        cycle_completeness = cycles_last_12_months / expected_cycles if expected_cycles > 0 else 0
        missing_cycle_score = 1 - cycle_completeness
        
        # Missed periods
        missed_period_score = min(missed_period_frequency / 12, 1.0)
        
        # Combined irregularity score
        irregularity = (cycle_deviation * 0.3 + missing_cycle_score * 0.4 + missed_period_score * 0.3)
        return min(irregularity, 1.0)
    
    @staticmethod
    def calculate_ovulation_risk_score(cycle_length_avg: float, cycles_last_12_months: int,
                                      missed_period_frequency: int) -> float:
        """
        Calculate ovulation risk score (0-1)
        Higher value = higher risk of anovulation
        """
        # Very short or very long cycles suggest anovulation
        if cycle_length_avg < 21 or cycle_length_avg > 35:
            cycle_risk = 0.8
        elif cycle_length_avg < 24 or cycle_length_avg > 32:
            cycle_risk = 0.5
        else:
            cycle_risk = 0.2
        
        # Missing cycles
        missing_cycles = 12 - cycles_last_12_months
        missing_risk = min(missing_cycles / 12, 1.0)
        
        # Missed periods
        missed_risk = min(missed_period_frequency / 12, 1.0)
        
        ovulation_risk = (cycle_risk * 0.4 + missing_risk * 0.3 + missed_risk * 0.3)
        return min(ovulation_risk, 1.0)
    
    @staticmethod
    def calculate_hyperandrogenism_score(acne_severity: int, facial_hair_growth: int,
                                        hair_thinning: int, dark_patches_skin: bool) -> float:
        """
        Calculate hyperandrogenism score (0-1)
        Higher value = more signs of high androgen levels
        """
        # Normalize symptom scores (0-5 scale)
        acne_norm = acne_severity / 5.0
        facial_hair_norm = facial_hair_growth / 5.0
        hair_thinning_norm = hair_thinning / 5.0
        dark_patches_norm = 1.0 if dark_patches_skin else 0.0
        
        # Weighted combination
        hyperandrogenism = (
            acne_norm * 0.3 +
            facial_hair_norm * 0.3 +
            hair_thinning_norm * 0.2 +
            dark_patches_norm * 0.2
        )
        return min(hyperandrogenism, 1.0)
    
    @staticmethod
    def calculate_metabolic_risk_score(bmi: float, fatigue_level: int, sugar_cravings: int,
                                      sudden_weight_gain: bool) -> float:
        """
        Calculate metabolic risk score (0-1)
        Higher value = higher metabolic risk
        """
        # BMI risk (normal BMI is 18.5-24.9)
        if bmi < 18.5:
            bmi_risk = 0.2
        elif bmi < 25:
            bmi_risk = 0.3
        elif bmi < 30:
            bmi_risk = 0.6
        else:
            bmi_risk = 0.9
        bmi_norm = bmi_risk
        
        # Fatigue (0-5 scale)
        fatigue_norm = fatigue_level / 5.0
        
        # Sugar cravings (0-5 scale)
        sugar_norm = sugar_cravings / 5.0
        
        # Weight gain
        weight_gain_norm = 1.0 if sudden_weight_gain else 0.0
        
        metabolic_risk = (
            bmi_norm * 0.4 +
            fatigue_norm * 0.2 +
            sugar_norm * 0.2 +
            weight_gain_norm * 0.2
        )
        return min(metabolic_risk, 1.0)
    
    @staticmethod
    def calculate_lifestyle_risk_score(stress_level: int, sleep_hours: float,
                                      exercise_days_per_week: int) -> float:
        """
        Calculate lifestyle risk score (0-1)
        Higher value = higher lifestyle-related risk
        """
        # Stress (0-10 scale)
        stress_norm = stress_level / 10.0
        
        # Sleep (optimal is 7-9 hours)
        if 7 <= sleep_hours <= 9:
            sleep_risk = 0.2
        elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
            sleep_risk = 0.5
        else:
            sleep_risk = 0.8
        sleep_norm = sleep_risk
        
        # Exercise (optimal is 3-5 days per week)
        if exercise_days_per_week >= 3:
            exercise_risk = 0.2
        elif exercise_days_per_week >= 1:
            exercise_risk = 0.5
        else:
            exercise_risk = 0.8
        exercise_norm = exercise_risk
        
        lifestyle_risk = (
            stress_norm * 0.4 +
            sleep_norm * 0.3 +
            exercise_norm * 0.3
        )
        return min(lifestyle_risk, 1.0)
    
    @staticmethod
    def engineer_features(data: Dict[str, Any]) -> Dict[str, float]:
        """
        Engineer all features from input data
        Returns normalized feature dictionary
        """
        # Calculate BMI
        bmi = FeatureEngineer.calculate_bmi(data['weight_kg'], data['height_cm'])
        
        # Calculate risk scores
        cycle_irregularity = FeatureEngineer.calculate_cycle_irregularity_index(
            data['cycle_length_avg'],
            data['cycles_last_12_months'],
            data['missed_period_frequency']
        )
        
        ovulation_risk = FeatureEngineer.calculate_ovulation_risk_score(
            data['cycle_length_avg'],
            data['cycles_last_12_months'],
            data['missed_period_frequency']
        )
        
        hyperandrogenism = FeatureEngineer.calculate_hyperandrogenism_score(
            data['acne_severity'],
            data['facial_hair_growth'],
            data['hair_thinning'],
            data['dark_patches_skin']
        )
        
        metabolic_risk = FeatureEngineer.calculate_metabolic_risk_score(
            bmi,
            data['fatigue_level'],
            data['sugar_cravings'],
            data['sudden_weight_gain']
        )
        
        lifestyle_risk = FeatureEngineer.calculate_lifestyle_risk_score(
            data['stress_level'],
            data['sleep_hours'],
            data['exercise_days_per_week']
        )
        
        # Normalize BMI (0-1 scale, assuming max BMI of 50)
        bmi_norm = min(bmi / 50.0, 1.0)
        
        # Normalize cycle length (0-1 scale)
        cycle_length_norm = min(data['cycle_length_avg'] / 50.0, 1.0)
        
        # Family history (0 or 1)
        family_history_norm = 1.0 if data['family_history_pcos'] else 0.0
        
        # Age normalization (assuming relevant range 13-50)
        age_norm = (data['age'] - 13) / (50 - 13)
        
        return {
            'bmi': bmi_norm,
            'bmi_raw': bmi,
            'cycle_irregularity': cycle_irregularity,
            'ovulation_risk': ovulation_risk,
            'hyperandrogenism': hyperandrogenism,
            'metabolic_risk': metabolic_risk,
            'lifestyle_risk': lifestyle_risk,
            'cycle_length_norm': cycle_length_norm,
            'family_history': family_history_norm,
            'age_norm': age_norm,
            'cycles_completeness': data['cycles_last_12_months'] / 12.0,
            'missed_periods_norm': min(data['missed_period_frequency'] / 12.0, 1.0)
        }

