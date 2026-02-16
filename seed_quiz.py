"""
Seed Quiz Questions Database
Run this script to populate the quiz_questions table with PCOS awareness questions
"""
from app.database import SessionLocal, engine, Base
from app.models import QuizQuestion
import json

# Create all tables
Base.metadata.create_all(bind=engine)

# Quiz questions data
QUIZ_QUESTIONS = [
    {
        "question": "What does PCOS stand for?",
        "options": ["Polycystic Ovary Syndrome", "Polycystic Ovarian System", "Poly Cystic Organ Syndrome", "Polycystic Ovulation Syndrome"],
        "correct_answer": "Polycystic Ovary Syndrome"
    },
    {
        "question": "Which hormone imbalance is most commonly associated with PCOS?",
        "options": ["Estrogen", "Progesterone", "Androgens (male hormones)", "Thyroid hormones"],
        "correct_answer": "Androgens (male hormones)"
    },
    {
        "question": "What percentage of women of reproductive age are affected by PCOS?",
        "options": ["1-3%", "5-10%", "15-20%", "25-30%"],
        "correct_answer": "5-10%"
    },
    {
        "question": "Which of the following is NOT a common symptom of PCOS?",
        "options": ["Irregular periods", "Excessive hair growth", "Weight gain", "Frequent headaches"],
        "correct_answer": "Frequent headaches"
    },
    {
        "question": "What is insulin resistance in relation to PCOS?",
        "options": [
            "When the body doesn't produce insulin",
            "When cells don't respond properly to insulin",
            "When insulin levels are too low",
            "When the pancreas stops working"
        ],
        "correct_answer": "When cells don't respond properly to insulin"
    },
    {
        "question": "Which lifestyle change is most recommended for managing PCOS?",
        "options": ["Increasing sugar intake", "Regular exercise and balanced diet", "Avoiding all carbohydrates", "Taking vitamin supplements only"],
        "correct_answer": "Regular exercise and balanced diet"
    },
    {
        "question": "Can PCOS affect fertility?",
        "options": ["No, it has no effect", "Yes, it can make it harder to conceive", "Only in severe cases", "It improves fertility"],
        "correct_answer": "Yes, it can make it harder to conceive"
    },
    {
        "question": "What is the Rotterdam criteria used for?",
        "options": ["Treating PCOS", "Diagnosing PCOS", "Preventing PCOS", "Curing PCOS"],
        "correct_answer": "Diagnosing PCOS"
    },
    {
        "question": "Which type of diet is often recommended for PCOS management?",
        "options": ["High sugar diet", "Low glycemic index diet", "High fat diet", "Liquid diet only"],
        "correct_answer": "Low glycemic index diet"
    },
    {
        "question": "Is PCOS curable?",
        "options": [
            "Yes, with medication",
            "Yes, with surgery",
            "No, but symptoms can be managed",
            "Yes, it goes away on its own"
        ],
        "correct_answer": "No, but symptoms can be managed"
    },
    {
        "question": "What role does stress play in PCOS?",
        "options": [
            "No role at all",
            "It can worsen symptoms",
            "It cures PCOS",
            "It only affects mood"
        ],
        "correct_answer": "It can worsen symptoms"
    },
    {
        "question": "Which specialist should you consult for PCOS?",
        "options": ["Cardiologist", "Dermatologist", "Gynecologist or Endocrinologist", "Neurologist"],
        "correct_answer": "Gynecologist or Endocrinologist"
    },
    {
        "question": "Can PCOS increase the risk of other health conditions?",
        "options": [
            "No",
            "Yes, including diabetes and heart disease",
            "Only in older women",
            "Only if untreated for 10+ years"
        ],
        "correct_answer": "Yes, including diabetes and heart disease"
    },
    {
        "question": "What is hirsutism?",
        "options": [
            "Hair loss on the scalp",
            "Excessive hair growth in a male pattern",
            "Premature graying",
            "Brittle hair"
        ],
        "correct_answer": "Excessive hair growth in a male pattern"
    },
    {
        "question": "Which blood test is commonly used to diagnose PCOS?",
        "options": [
            "Complete blood count",
            "Hormone level tests",
            "Cholesterol test",
            "Liver function test"
        ],
        "correct_answer": "Hormone level tests"
    }
]


def seed_quiz_questions():
    """Seed the database with quiz questions"""
    db = SessionLocal()
    
    try:
        # Check if questions already exist
        existing_count = db.query(QuizQuestion).count()
        
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} quiz questions.")
            response = input("Do you want to clear and re-seed? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return
            
            # Clear existing questions
            db.query(QuizQuestion).delete()
            db.commit()
            print("✓ Cleared existing questions")
        
        # Add new questions
        for q_data in QUIZ_QUESTIONS:
            question = QuizQuestion(
                question=q_data["question"],
                options=json.dumps(q_data["options"]),  # Store as JSON string
                correct_answer=q_data["correct_answer"]
            )
            db.add(question)
        
        db.commit()
        print(f"✓ Successfully seeded {len(QUIZ_QUESTIONS)} quiz questions!")
        
        # Verify
        total = db.query(QuizQuestion).count()
        print(f"✓ Total questions in database: {total}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding PCOS Awareness Quiz Questions...")
    print("=" * 50)
    seed_quiz_questions()
    print("=" * 50)
    print("✓ Done!")
