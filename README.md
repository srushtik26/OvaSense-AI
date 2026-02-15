# OvaSense AI - PCOS Risk & Phenotype Detection System

A complete end-to-end AI-powered system for PCOS risk assessment and phenotype detection. This system combines medical insights with machine learning to provide personalized risk assessments and lifestyle recommendations.

## ⚠️ Important Disclaimer

**This system does NOT diagnose PCOS.** It provides risk assessment, pattern detection, and probability estimates based on self-reported data. Always consult a qualified healthcare professional for proper medical evaluation and diagnosis.

## Features

- 🔒 **Safe & Private**: Your data is secure and private
- 🤖 **AI-Powered**: Advanced pattern detection using machine learning
- 🎯 **Personalized**: Tailored recommendations based on your unique profile
- 📊 **Comprehensive**: Risk assessment with phenotype identification
- 📄 **Report Generation**: Downloadable PDF reports for doctor consultations
- 💡 **Explainable AI**: Understand why you received your assessment

## System Architecture

### Backend (FastAPI)
- **API Layer**: RESTful endpoints for assessments
- **Feature Engineering**: Medical feature calculation (BMI, cycle irregularity, risk scores)
- **Risk Detection**: Hybrid rule-based + ML clustering approach
- **Explainable AI**: Feature attribution and explanations
- **Remedy Engine**: Personalized lifestyle recommendations
- **Report Generator**: PDF report creation

### Frontend (Next.js/React)
- **Welcome Screen**: Introduction and feature overview
- **Smart Questionnaire**: Step-based data collection
- **Results Dashboard**: Comprehensive results display
- **Report Download**: PDF generation and download

## Tech Stack

### Backend
- FastAPI
- PostgreSQL (SQLAlchemy)
- scikit-learn
- pandas, numpy
- HDBSCAN (clustering)
- SHAP (explainable AI)
- ReportLab (PDF generation)

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios
- React Hook Form
- Framer Motion

## Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+

### Backend Setup

1. Clone the repository and navigate to the project directory:
```bash
cd pcod
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Create the database:
```bash
# Using PostgreSQL
createdb ovasense_db
```

6. Run the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### POST `/api/v1/assessments/analyze`
Submit an assessment and get risk analysis.

**Request Body:**
```json
{
  "age": 25,
  "height_cm": 165,
  "weight_kg": 70,
  "family_history_pcos": false,
  "cycle_length_avg": 35,
  "cycles_last_12_months": 8,
  "missed_period_frequency": 4,
  "period_flow_type": "normal",
  "acne_severity": 3,
  "facial_hair_growth": 2,
  "hair_thinning": 1,
  "dark_patches_skin": false,
  "sudden_weight_gain": true,
  "fatigue_level": 4,
  "sugar_cravings": 4,
  "stress_level": 7,
  "sleep_hours": 6.5,
  "exercise_days_per_week": 2,
  "diet_type": "vegetarian"
}
```

**Response:**
```json
{
  "risk_level": "Moderate",
  "phenotype": "Insulin-Resistant Pattern",
  "confidence": "84%",
  "risk_score": 65.2,
  "key_drivers": [
    "Irregular cycles",
    "High BMI",
    "Acne severity"
  ],
  "remedies": [
    "Reduce refined sugar and processed foods",
    "Focus on low-glycemic index foods",
    "Aim for 30 minutes of moderate exercise daily",
    "Maintain consistent meal times"
  ],
  "next_steps": [
    "Schedule consultation with gynecologist",
    "Consider hormone panel testing",
    "Track cycles for 3 months"
  ],
  "disclaimer": "This is not a medical diagnosis. Please consult a doctor for confirmation."
}
```

### GET `/api/v1/assessments/{assessment_id}`
Retrieve a saved assessment by ID.

### GET `/api/v1/assessments/{assessment_id}/report`
Download PDF report for an assessment.

### GET `/api/v1/assessments/user/{user_id}/history`
Get assessment history for a user.

## Risk Detection Logic

The system uses a hybrid approach:

1. **Rule-Based Screening**: Identifies high suspicion cases based on:
   - Irregular cycles (cycle irregularity > 0.5)
   - High androgen symptoms (hyperandrogenism > 0.4)

2. **ML Clustering**: Identifies phenotype patterns:
   - Insulin-Resistant Pattern
   - Hyperandrogenic Pattern
   - Inflammatory Pattern
   - Stress-Driven Pattern
   - Mixed Pattern

3. **Risk Scoring**: Combines multiple factors:
   - Cycle irregularity
   - Hyperandrogenism
   - Metabolic risk
   - Ovulation risk
   - Lifestyle risk

## Phenotype Patterns

### Insulin-Resistant Pattern
- High metabolic risk factors
- Elevated BMI
- Cycle irregularity
- Recommendations focus on diet and exercise

### Hyperandrogenic Pattern
- High androgen symptoms (acne, hair growth)
- Cycle irregularity
- Recommendations focus on hormonal balance

### Inflammatory Pattern
- Combination of inflammatory factors
- Recommendations focus on anti-inflammatory diet

### Stress-Driven Pattern
- High lifestyle risk (stress, sleep)
- Recommendations focus on stress management

### Mixed Pattern
- Multiple contributing factors
- Comprehensive approach needed

## Safety Features

- ✅ No medical diagnosis
- ✅ Risk assessment only
- ✅ Clear disclaimers throughout
- ✅ Encourages doctor consultation
- ✅ Transparent explanations

## Development

### Running Tests
```bash
# Backend tests (when implemented)
pytest

# Frontend tests (when implemented)
npm test
```

### Code Structure
```
pcod/
├── app/
│   ├── api/           # API endpoints
│   ├── services/      # Business logic
│   ├── models.py      # Database models
│   ├── schemas.py     # Pydantic schemas
│   ├── database.py    # Database configuration
│   └── main.py        # FastAPI app
├── frontend/
│   ├── app/           # Next.js app directory
│   ├── components/    # React components
│   └── public/        # Static assets
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## License

This project is for educational and informational purposes only. Not intended for medical use.

## Contributing

Contributions are welcome! Please ensure all code follows the safety guidelines and includes appropriate disclaimers.

## Support

For issues or questions, please open an issue on the repository.

---

**Remember**: This tool is for informational purposes only. Always consult with a qualified healthcare professional for medical advice.

