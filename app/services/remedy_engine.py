from typing import List, Dict

class RemedyEngine:
    """Personalized lifestyle remedy recommendations based on phenotype"""
    
    REMEDIES_BY_PHENOTYPE = {
        "Insulin-resistant PCOS": {
            "diet": [
                "Reduce refined sugar and processed foods",
                "Focus on low-glycemic index foods (whole grains, vegetables)",
                "Include protein with every meal",
                "Limit fruit intake to 1-2 servings per day",
                "Consider intermittent fasting (consult doctor first)"
            ],
            "exercise": [
                "Aim for 30 minutes of moderate exercise daily",
                "Include both cardio and strength training",
                "Walking after meals can help with insulin sensitivity",
                "Start with 10-15 minutes and gradually increase"
            ],
            "lifestyle": [
                "Maintain consistent meal times",
                "Prioritize 7-9 hours of quality sleep",
                "Manage portion sizes",
                "Stay hydrated throughout the day"
            ],
            "supplements": [
                "Consider inositol (consult doctor first)",
                "Vitamin D if deficient",
                "Omega-3 fatty acids"
            ]
        },
        "Inflammatory PCOS": {
            "diet": [
                "Anti-inflammatory foods (turmeric, ginger, green leafy vegetables)",
                "Omega-3 rich foods (fatty fish, walnuts, flaxseeds)",
                "Reduce processed foods and trans fats",
                "Include probiotic foods (yogurt, kefir, fermented foods)",
                "Limit inflammatory foods (sugar, refined carbs, processed meats)"
            ],
            "exercise": [
                "Regular moderate exercise",
                "Yoga for stress and inflammation reduction",
                "Avoid excessive high-intensity workouts"
            ],
            "lifestyle": [
                "Prioritize gut health",
                "Manage stress effectively",
                "Ensure quality sleep",
                "Consider anti-inflammatory practices (meditation, breathing exercises)"
            ],
            "supplements": [
                "Omega-3 supplements",
                "Probiotics",
                "Turmeric/curcumin (consult doctor)",
                "Vitamin D"
            ]
        },
        "Adrenal PCOS": {
            "diet": [
                "Regular, balanced meals to stabilize blood sugar",
                "Include magnesium-rich foods (dark leafy greens, nuts, seeds)",
                "Limit caffeine, especially in the afternoon",
                "Avoid skipping meals"
            ],
            "exercise": [
                "Gentle to moderate exercise (yoga, walking, swimming)",
                "Avoid over-exercising",
                "Focus on stress-reducing activities",
                "3-4 days per week is sufficient"
            ],
            "lifestyle": [
                "Establish a consistent sleep schedule (7-9 hours)",
                "Practice stress management (meditation, deep breathing, journaling)",
                "Create work-life balance boundaries",
                "Consider therapy or counseling if stress is overwhelming",
                "Limit screen time before bed"
            ],
            "supplements": [
                "Magnesium (consult doctor)",
                "Adaptogenic herbs (ashwagandha, rhodiola - consult doctor)",
                "B-complex vitamins"
            ]
        }
    }
    
    CLINICAL_NEXT_STEPS = {
        "Low": [
            "Continue monitoring your cycles and symptoms",
            "Maintain healthy lifestyle habits",
            "Consider annual check-up with gynecologist",
            "Track cycles for 3 months to establish baseline"
        ],
        "Moderate": [
            "Schedule consultation with gynecologist or endocrinologist",
            "Consider hormone panel testing (FSH, LH, testosterone, insulin)",
            "Track cycles and symptoms for 3 months",
            "Discuss lifestyle modifications with healthcare provider",
            "Consider ultrasound if recommended by doctor"
        ],
        "High": [
            "Schedule consultation with gynecologist or endocrinologist as soon as possible",
            "Request comprehensive hormone panel (FSH, LH, testosterone, DHEA-S, insulin, glucose)",
            "Consider pelvic ultrasound to check for ovarian morphology",
            "Discuss treatment options with healthcare provider",
            "Monitor cycles and symptoms closely",
            "Consider working with a registered dietitian specializing in hormonal health"
        ]
    }
    
    @staticmethod
    def get_remedies(phenotype: str, risk_level: str) -> Dict[str, List[str]]:
        """
        Get personalized remedies based on phenotype
        Returns dictionary with diet, exercise, lifestyle, and supplements
        """
        remedies = RemedyEngine.REMEDIES_BY_PHENOTYPE.get(
            phenotype,
            RemedyEngine.REMEDIES_BY_PHENOTYPE["Insulin-resistant PCOS"]
        )
        
        return {
            "diet": remedies["diet"],
            "exercise": remedies["exercise"],
            "lifestyle": remedies["lifestyle"],
            "supplements": remedies["supplements"]
        }
    
    @staticmethod
    def get_combined_remedies_list(phenotype: str, risk_level: str) -> List[str]:
        """
        Get a simplified list of top remedies for API response
        """
        remedies = RemedyEngine.get_remedies(phenotype, risk_level)
        
        # Combine top recommendations from each category
        combined = []
        
        # Top 2 from diet
        combined.extend(remedies["diet"][:2])
        
        # Top 1 from exercise
        combined.extend(remedies["exercise"][:1])
        
        # Top 1 from lifestyle
        combined.extend(remedies["lifestyle"][:1])
        
        return combined
    
    @staticmethod
    def get_clinical_next_steps(risk_level: str) -> List[str]:
        """
        Get clinical next steps based on risk level
        """
        return RemedyEngine.CLINICAL_NEXT_STEPS.get(
            risk_level,
            RemedyEngine.CLINICAL_NEXT_STEPS["Moderate"]
        )

