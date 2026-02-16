# 🚀 OvaSense AI v2.0 - Complete Setup Guide

## 📋 Prerequisites

- **Backend**: Python 3.8+, PostgreSQL
- **Frontend**: Node.js 18+, npm

---

## 🔧 Backend Setup

### 1. Navigate to backend directory
```bash
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod
```

### 2. Activate virtual environment
```bash
.\venv\Scripts\activate
```

### 3. Install dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

### 4. Configure database
Ensure `.env` file exists with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/ovasense_db
```

### 5. Create database tables
```bash
python init_db.py
```

### 6. Seed quiz questions
```bash
python seed_quiz.py
```

### 7. Start backend server
```bash
python -m uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**

---

## 🎨 Frontend Setup

### 1. Navigate to frontend directory
```bash
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod\frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start development server
```bash
npm run dev
```

Frontend will run on: **http://localhost:3000**

---

## ✅ Verification

### Backend Health Check
Visit: http://localhost:8000/health
Expected: `{"status": "healthy"}`

### API Documentation
Visit: http://localhost:8000/docs
You should see all 11 new endpoints + existing assessment endpoints

### Frontend
Visit: http://localhost:3000
You should see the landing page with "Get Started" button

### Dashboard
Visit: http://localhost:3000/dashboard/home
You should see the complete dashboard with sidebar navigation

---

## 🎯 Complete User Flow Test

1. **Landing Page** → http://localhost:3000
   - Click "Get Started"

2. **Dashboard Home** → http://localhost:3000/dashboard/home
   - View health score widget
   - See quick stats
   - Check quick action buttons

3. **Take Assessment** → Click sidebar "Assessment"
   - Click "Start Assessment"
   - Complete the assessment form
   - View results

4. **Period Tracker** → Click sidebar "Period Tracker"
   - Add a period log
   - View cycle statistics
   - Check prediction

5. **Mental Health** → Click sidebar "Mental Health"
   - Complete daily check-in
   - View averages
   - Read AI insights

6. **Diet Plan** → Click sidebar "Diet Plan"
   - View personalized recommendations
   - Browse weekly meal plan
   - Read nutritional tips

7. **Quiz** → Click sidebar "Quiz"
   - Answer questions
   - Submit quiz
   - View score and tips

8. **Reports** → Click sidebar "Reports"
   - View monthly summary
   - Check trends
   - See achievements

---

## 📁 Project Structure

```
pcod/
├── app/                          # Backend (FastAPI)
│   ├── api/                      # API routes (11 endpoints)
│   ├── services/                 # Business logic (6 new services)
│   ├── models.py                 # Database models
│   ├── schemas.py                # Pydantic schemas
│   └── main.py                   # FastAPI app
│
└── frontend/                     # Frontend (Next.js)
    ├── app/
    │   ├── page.tsx              # Landing page
    │   └── dashboard/            # Dashboard pages
    │       ├── layout.tsx        # Dashboard shell
    │       ├── home/             # Tab 1: Home
    │       ├── assessment/       # Tab 2: Assessment
    │       ├── period/           # Tab 3: Period Tracker
    │       ├── mental-health/    # Tab 4: Mental Health
    │       ├── diet/             # Tab 5: Diet Plan
    │       ├── quiz/             # Tab 6: Quiz
    │       └── reports/          # Tab 7: Reports
    ├── components/
    │   ├── layout/               # Sidebar, Header
    │   └── ui/                   # Button, Card, LoadingSpinner
    ├── lib/
    │   ├── api.ts                # API client
    │   ├── utils.ts              # Utility functions
    │   └── hooks/                # Custom React hooks
    └── context/
        └── UserContext.tsx       # Global state
```

---

## 🎨 Features Implemented

### Backend (v2.0)
✅ Health Score Engine
✅ Period Tracker with predictions
✅ Mental Health Tracker with AI insights
✅ AI Diet Personalizer
✅ PCOS Awareness Quiz (15 questions)
✅ Monthly Progress Reports
✅ 11 new API endpoints
✅ 4 new database tables

### Frontend (v2.0)
✅ Complete dashboard with 7 tabs
✅ Sidebar navigation
✅ Health score visualization
✅ Period tracking forms
✅ Mental health check-in
✅ Interactive quiz
✅ Weekly meal planner
✅ Monthly reports
✅ Responsive design
✅ Toast notifications
✅ Loading states

---

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error**
```bash
# Verify PostgreSQL is running
# Check DATABASE_URL in .env
```

**Import Errors**
```bash
# Activate virtual environment
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Issues

**Module Not Found**
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**API Connection Error**
```bash
# Verify backend is running on port 8000
# Check .env.local has correct API URL
```

**Port Already in Use**
```bash
# Frontend: Change port
npm run dev -- -p 3001

# Backend: Change port
uvicorn app.main:app --reload --port 8001
```

---

## 🚀 Production Deployment

### Backend
1. Set production DATABASE_URL
2. Disable debug mode
3. Add authentication
4. Deploy to cloud (AWS, GCP, Azure)

### Frontend
1. Build production bundle: `npm run build`
2. Deploy to Vercel/Netlify
3. Update API_URL to production backend

---

## 📊 Success Metrics

✅ Backend starts without errors
✅ All 11 new endpoints accessible
✅ Frontend loads in < 2 seconds
✅ All 7 dashboard tabs functional
✅ Forms submit successfully
✅ Data persists across sessions
✅ Responsive on mobile/tablet/desktop

---

## 🎉 You're All Set!

Your OvaSense AI v2.0 platform is ready!

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

Happy tracking! 💜
