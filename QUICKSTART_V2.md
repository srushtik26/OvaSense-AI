# 🚀 OvaSense AI v2.0 - Quick Start

## ⚡ Setup (3 Steps)

```bash
# 1. Activate virtual environment
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod
.\venv\Scripts\activate

# 2. Create tables & seed data
python init_db.py
python seed_quiz.py

# 3. Start server
python -m uvicorn app.main:app --reload
```

## 📍 Access Points

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 New Endpoints (All under `/api/v1/`)

| Feature | Endpoint |
|---------|----------|
| Health Score | `GET /health-score/{user_id}` |
| Add Period | `POST /period/add` |
| Period History | `GET /period/history/{user_id}` |
| Period Prediction | `GET /period/prediction/{user_id}` |
| Add Mental Health | `POST /mental-health/add` |
| Mental Health Insights | `GET /mental-health/insights/{user_id}` |
| Diet Plan | `GET /diet-plan/{user_id}` |
| Quiz Questions | `GET /quiz/questions` |
| Submit Quiz | `POST /quiz/submit` |
| Monthly Report | `GET /report/monthly/{user_id}` |

## 📦 What's New

✅ **6 New Modules**: Health Score, Period Tracker, Mental Health, Diet, Quiz, Reports
✅ **4 New Database Tables**: period_logs, mental_health_logs, quiz_questions, quiz_results
✅ **11 New API Endpoints**: All RESTful and documented
✅ **0 Breaking Changes**: Existing assessment API unchanged

## 📚 Documentation

- `UPGRADE_GUIDE.md` - Detailed setup & testing
- `API_DOCUMENTATION.md` - Complete API reference
- `walkthrough.md` - Implementation overview

## 🧪 Quick Test

```bash
# Test health score
curl http://localhost:8000/api/v1/health-score/user123

# Test quiz
curl http://localhost:8000/api/v1/quiz/questions
```

## ✨ Key Features

- **Health Score**: 0-100 score with weighted factors
- **Period Tracking**: Cycle analysis & predictions
- **Mental Health**: Stress trends & AI insights
- **Diet Plans**: Phenotype-specific recommendations
- **Quiz**: 15 PCOS awareness questions
- **Reports**: Monthly progress summaries

---

**Version**: 2.0.0 | **Status**: Ready for Testing
