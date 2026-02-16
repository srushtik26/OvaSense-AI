# 🎯 Quick Reference - OvaSense AI v2.0

## 🚀 Start Application

### Option 1: Manual Start (Recommended)

**Terminal 1 - Backend:**
```powershell
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod\frontend
npm run dev
```

### Option 2: PowerShell Script
```powershell
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod
.\START_APP.ps1
```

---

## 🌐 Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📁 Key Files

### Configuration
- `frontend/.env.local` - API URL configuration
- `.env` - Database connection (backend)

### Documentation
- `COMPLETE_SETUP_GUIDE.md` - Full setup instructions
- `TESTING_CHECKLIST.md` - Testing procedures
- `API_DOCUMENTATION.md` - API reference
- `walkthrough.md` - Implementation overview

### Scripts
- `init_db.py` - Initialize database
- `seed_quiz.py` - Seed quiz questions
- `START_APP.ps1` - Quick start script

---

## 🎨 Dashboard Tabs

1. **Home** - Health score & quick stats
2. **Assessment** - PCOS risk assessment
3. **Period Tracker** - Cycle tracking & predictions
4. **Mental Health** - Daily check-ins & AI insights
5. **Diet Plan** - Personalized PCOS nutrition
6. **Quiz** - PCOS awareness test
7. **Reports** - Monthly progress tracking

---

## ⚡ Quick Commands

### Backend
```powershell
# Activate venv
.\venv\Scripts\activate

# Run migrations
python init_db.py

# Seed quiz
python seed_quiz.py

# Start server
python -m uvicorn app.main:app --reload

# Test endpoint
curl http://localhost:8000/health
```

### Frontend
```powershell
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run production
npm start
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check if PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Activate virtual environment

### Frontend errors
- Run `npm install`
- Check `.env.local` has correct API_URL
- Clear browser cache

### No quiz questions
- Run `python seed_quiz.py`

### Health score shows 0
- Complete an assessment first
- Add period and mental health logs

---

## 📊 Features

### Backend (11 Endpoints)
✅ Health Score Engine
✅ Period Tracker with Predictions
✅ Mental Health Tracker with AI Insights
✅ AI Diet Personalizer
✅ PCOS Awareness Quiz
✅ Monthly Progress Reports

### Frontend (7 Dashboard Tabs)
✅ Complete UI with Sidebar Navigation
✅ Form Validation & Error Handling
✅ Toast Notifications
✅ Loading States
✅ Responsive Design
✅ Data Persistence

---

## 🎉 Success Indicators

✅ Backend: http://localhost:8000/health returns `{"status": "healthy"}`
✅ Frontend: http://localhost:3000 loads without errors
✅ Dashboard: All 7 tabs accessible
✅ Forms: Submit successfully with toast notifications
✅ Data: Persists across page refreshes

---

**Version**: 2.0.0  
**Status**: Production Ready ✅  
**Last Updated**: 2026-02-16
