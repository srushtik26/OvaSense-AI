"""
AI Diet Personalizer Service
Generates personalized diet plans based on PCOS phenotype, BMI, and symptoms
"""
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models import Assessment


class DietPersonalizerService:
    """Service for generating personalized diet recommendations"""
    
    # Diet recommendations by phenotype
    PHENOTYPE_DIETS = {
        "Insulin-Resistant PCOS": {
            "foods_to_eat": [
                "Leafy greens (spinach, kale, lettuce)",
                "Whole grains (quinoa, brown rice, oats)",
                "Lean proteins (chicken, fish, tofu)",
                "Nuts and seeds (almonds, chia seeds, flaxseeds)",
                "Berries (blueberries, strawberries)",
                "Legumes (lentils, chickpeas, black beans)",
                "Healthy fats (avocado, olive oil)",
                "Cinnamon (helps with insulin sensitivity)"
            ],
            "foods_to_avoid": [
                "White bread and refined carbs",
                "Sugary drinks and sodas",
                "Processed foods",
                "High-sugar fruits (mangoes, grapes in excess)",
                "Fried foods",
                "Artificial sweeteners",
                "Excessive dairy products"
            ],
            "tips": [
                "Focus on low glycemic index foods",
                "Eat protein with every meal",
                "Avoid sugar spikes by eating small, frequent meals",
                "Include fiber-rich foods to slow glucose absorption"
            ]
        },
        "Inflammatory PCOS": {
            "foods_to_eat": [
                "Fatty fish (salmon, mackerel, sardines)",
                "Turmeric and ginger",
                "Leafy greens and cruciferous vegetables",
                "Berries and cherries",
                "Olive oil and nuts",
                "Green tea",
                "Tomatoes",
                "Probiotic-rich foods (yogurt, kefir, kimchi)"
            ],
            "foods_to_avoid": [
                "Processed meats",
                "Trans fats and fried foods",
                "Refined sugars",
                "Excessive red meat",
                "Alcohol",
                "Gluten (if sensitive)",
                "High-omega-6 oils (corn, soybean)"
            ],
            "tips": [
                "Focus on anti-inflammatory foods",
                "Include omega-3 fatty acids daily",
                "Reduce inflammatory triggers",
                "Stay hydrated with water and herbal teas"
            ]
        },
        "Post-Pill PCOS": {
            "foods_to_eat": [
                "Cruciferous vegetables (broccoli, cauliflower)",
                "Zinc-rich foods (pumpkin seeds, oysters)",
                "Vitamin B-rich foods (eggs, leafy greens)",
                "Healthy fats (avocado, nuts)",
                "Fiber-rich foods",
                "Fermented foods for gut health",
                "Lean proteins"
            ],
            "foods_to_avoid": [
                "Processed foods",
                "Excessive caffeine",
                "Alcohol",
                "High-sugar foods",
                "Soy products (in excess)"
            ],
            "tips": [
                "Support hormone balance naturally",
                "Focus on liver detoxification foods",
                "Ensure adequate nutrient intake",
                "Consider seed cycling for hormone regulation"
            ]
        },
        "Adrenal PCOS": {
            "foods_to_eat": [
                "Vitamin C-rich foods (oranges, bell peppers)",
                "Magnesium-rich foods (dark chocolate, almonds)",
                "Complex carbohydrates (sweet potatoes, quinoa)",
                "Adaptogenic herbs (ashwagandha tea)",
                "Lean proteins",
                "Healthy fats",
                "Herbal teas (chamomile, lavender)"
            ],
            "foods_to_avoid": [
                "Excessive caffeine",
                "High-sugar foods",
                "Alcohol",
                "Processed foods",
                "Energy drinks"
            ],
            "tips": [
                "Focus on stress-reducing foods",
                "Avoid stimulants",
                "Eat regular meals to stabilize blood sugar",
                "Prioritize sleep and relaxation"
            ]
        }
    }
    
    @staticmethod
    def calculate_bmi(height_cm: float, weight_kg: float) -> float:
        """Calculate BMI"""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    @staticmethod
    def get_bmi_category(bmi: float) -> str:
        """Get BMI category"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    @staticmethod
    def generate_weekly_meal_plan(phenotype: str, bmi_category: str) -> Dict[str, List[str]]:
        """Generate a sample weekly meal plan"""
        
        # Base meal structure
        if phenotype == "Insulin-Resistant PCOS":
            return {
                "Monday": [
                    "Breakfast: Oatmeal with berries and chia seeds",
                    "Lunch: Grilled chicken salad with olive oil dressing",
                    "Dinner: Baked salmon with quinoa and steamed broccoli",
                    "Snacks: Almonds, Greek yogurt"
                ],
                "Tuesday": [
                    "Breakfast: Scrambled eggs with spinach and whole grain toast",
                    "Lunch: Lentil soup with mixed vegetables",
                    "Dinner: Stir-fried tofu with brown rice and vegetables",
                    "Snacks: Apple slices with almond butter"
                ],
                "Wednesday": [
                    "Breakfast: Greek yogurt with flaxseeds and berries",
                    "Lunch: Quinoa bowl with chickpeas and roasted vegetables",
                    "Dinner: Grilled fish with sweet potato and green beans",
                    "Snacks: Carrot sticks with hummus"
                ],
                "Remaining Days": [
                    "Continue rotating similar low-GI, high-protein meals",
                    "Focus on portion control and meal timing",
                    "Stay hydrated with water and herbal teas"
                ]
            }
        elif phenotype == "Inflammatory PCOS":
            return {
                "Monday": [
                    "Breakfast: Smoothie with berries, spinach, and flaxseeds",
                    "Lunch: Salmon salad with mixed greens and olive oil",
                    "Dinner: Turmeric chicken with roasted vegetables",
                    "Snacks: Walnuts, green tea"
                ],
                "Tuesday": [
                    "Breakfast: Chia pudding with berries",
                    "Lunch: Quinoa bowl with grilled vegetables and tahini",
                    "Dinner: Baked mackerel with sweet potato",
                    "Snacks: Anti-inflammatory smoothie"
                ],
                "Remaining Days": [
                    "Focus on omega-3 rich foods",
                    "Include turmeric and ginger in meals",
                    "Drink green tea regularly"
                ]
            }
        else:
            return {
                "General Plan": [
                    "Breakfast: Protein-rich options with vegetables",
                    "Lunch: Balanced meals with lean protein and complex carbs",
                    "Dinner: Light, nutrient-dense meals",
                    "Snacks: Nuts, seeds, fruits"
                ]
            }
    
    @staticmethod
    def generate_diet_plan(db: Session, user_id: str) -> Dict:
        """Generate personalized diet plan"""
        
        # Get latest assessment
        assessment = db.query(Assessment).filter(
            Assessment.user_id == user_id
        ).order_by(Assessment.created_at.desc()).first()
        
        if not assessment:
            return {
                "phenotype": "Unknown",
                "bmi_category": "Unknown",
                "foods_to_eat": ["Complete an assessment first to get personalized recommendations"],
                "foods_to_avoid": [],
                "weekly_meal_plan": {},
                "nutritional_tips": ["Take the PCOS assessment to receive a customized diet plan"]
            }
        
        # Calculate BMI
        bmi = DietPersonalizerService.calculate_bmi(assessment.height_cm, assessment.weight_kg)
        bmi_category = DietPersonalizerService.get_bmi_category(bmi)
        
        phenotype = assessment.phenotype or "Insulin-Resistant PCOS"
        
        # Get diet recommendations for phenotype
        diet_data = DietPersonalizerService.PHENOTYPE_DIETS.get(
            phenotype,
            DietPersonalizerService.PHENOTYPE_DIETS["Insulin-Resistant PCOS"]
        )
        
        # Generate meal plan
        meal_plan = DietPersonalizerService.generate_weekly_meal_plan(phenotype, bmi_category)
        
        # Add BMI-specific tips
        additional_tips = []
        if bmi_category == "Overweight" or bmi_category == "Obese":
            additional_tips.extend([
                "Focus on portion control",
                "Aim for a caloric deficit through balanced nutrition",
                "Increase physical activity gradually"
            ])
        elif bmi_category == "Underweight":
            additional_tips.extend([
                "Ensure adequate caloric intake",
                "Focus on nutrient-dense foods",
                "Consider healthy weight gain strategies"
            ])
        
        return {
            "phenotype": phenotype,
            "bmi_category": bmi_category,
            "foods_to_eat": diet_data["foods_to_eat"],
            "foods_to_avoid": diet_data["foods_to_avoid"],
            "weekly_meal_plan": meal_plan,
            "nutritional_tips": diet_data["tips"] + additional_tips
        }
