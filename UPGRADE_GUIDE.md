# 🚀 OvaSense AI v2.0 - Setup & Testing Guide

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment activated

## 🔧 Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Ensure your `.env` file has the correct database URL:
```
DATABASE_URL=postgresql://user:password@localhost:5432/ovasense_db
```

### 3. Create Database Tables
```bash
python init_db.py
```

This will create all tables including:
- `assessments` (existing)
- `period_logs` (new)
- `mental_health_logs` (new)
- `quiz_questions` (new)
- `quiz_results` (new)

### 4. Seed Quiz Questions
```bash
python seed_quiz.py
```

This populates the database with 15 PCOS awareness quiz questions.

### 5. Start the Backend
```bash
python -m uvicorn app.main:app --reload
```

Or use the batch file:
```bash
run_backend.bat
```

## 🧪 Testing the New APIs

### Test Health Score
```bash
curl http://localhost:8000/api/v1/health-score/user123
```

### Test Period Tracker
```bash
# Add period log
curl -X POST http://localhost:8000/api/v1/period/add \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "start_date": "2026-02-01",
    "end_date": "2026-02-05",
    "flow_type": "normal",
    "pain_level": 5,
    "mood": "irritable"
  }'

# Get history
curl http://localhost:8000/api/v1/period/history/user123

# Get prediction
curl http://localhost:8000/api/v1/period/prediction/user123
```

### Test Mental Health Tracker
```bash
# Add mental health log
curl -X POST http://localhost:8000/api/v1/mental-health/add \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "stress_level": 7,
    "mood_type": "anxious",
    "sleep_hours": 6.5,
    "energy_level": 4
  }'

# Get insights
curl http://localhost:8000/api/v1/mental-health/insights/user123
```

### Test Diet Plan
```bash
curl http://localhost:8000/api/v1/diet-plan/user123
```

### Test Quiz
```bash
# Get questions
curl http://localhost:8000/api/v1/quiz/questions

# Submit quiz
curl -X POST http://localhost:8000/api/v1/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "answers": {
      "1": "Polycystic Ovary Syndrome",
      "2": "Androgens (male hormones)"
    }
  }'
```

### Test Monthly Report
```bash
curl http://localhost:8000/api/v1/report/monthly/user123
```

## 📊 Interactive API Documentation

Visit these URLs after starting the server:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ✅ Verification Checklist

- [ ] All database tables created successfully
- [ ] Quiz questions seeded (15 questions)
- [ ] Backend starts without errors
- [ ] All 6 new API modules accessible:
  - [ ] Health Score API
  - [ ] Period Tracker API
  - [ ] Mental Health API
  - [ ] Diet Plan API
  - [ ] Quiz API
  - [ ] Reports API
- [ ] Existing assessment API still works
- [ ] Swagger documentation shows all endpoints

## 🎯 Complete User Flow Test

1. **Create Assessment** (existing feature)
   - POST `/api/v1/assessments/`
   - Note the `user_id` from response

2. **Get Health Score**
   - GET `/api/v1/health-score/{user_id}`

3. **Log Period**
   - POST `/api/v1/period/add`

4. **Track Mental Health**
   - POST `/api/v1/mental-health/add`

5. **Get Diet Plan**
   - GET `/api/v1/diet-plan/{user_id}`

6. **Take Quiz**
   - GET `/api/v1/quiz/questions`
   - POST `/api/v1/quiz/submit`

7. **View Monthly Report**
   - GET `/api/v1/report/monthly/{user_id}`

## 🐛 Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check `.env` file has correct credentials
- Ensure database exists

### Import Errors
- Activate virtual environment
- Run `pip install -r requirements.txt`

### Port Already in Use
- Change port: `uvicorn app.main:app --reload --port 8001`

## 📁 Project Structure

```
pcod/
├── app/
│   ├── api/
│   │   ├── __init__.py          # Router registration
│   │   ├── assessments.py       # Existing
│   │   ├── health_score.py      # NEW
│   │   ├── period.py            # NEW
│   │   ├── mental_health.py     # NEW
│   │   ├── diet.py              # NEW
│   │   ├── quiz.py              # NEW
│   │   └── reports.py           # NEW
│   ├── services/
│   │   ├── health_score_engine.py      # NEW
│   │   ├── period_tracker.py           # NEW
│   │   ├── mental_health_tracker.py    # NEW
│   │   ├── diet_personalizer.py        # NEW
│   │   ├── quiz_engine.py              # NEW
│   │   └── report_progress.py          # NEW
│   ├── models.py            # Updated with 4 new models
│   ├── schemas.py           # Updated with new schemas
│   ├── database.py          # Unchanged
│   └── main.py              # Updated to v2.0.0
├── seed_quiz.py             # NEW - Quiz seeding script
├── init_db.py               # Existing
└── requirements.txt         # Existing
```

## 🎉 Success Indicators

✅ Backend starts with message: "OvaSense AI API v2.0.0"
✅ Swagger docs show 6 new API sections
✅ Database has 5 tables (1 existing + 4 new)
✅ Quiz database has 15 questions
✅ All endpoints return proper JSON responses
✅ No breaking changes to existing assessment API

## 📞 Next Steps

1. Test all endpoints thoroughly
2. Integrate with Next.js frontend
3. Add user authentication
4. Implement PDF generation for reports
5. Add data visualization for trends
6. Deploy to production

---

**Note**: This is a major upgrade from v1.0 to v2.0. All existing functionality is preserved while adding 6 new engagement modules!
