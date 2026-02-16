# 🚀 OvaSense AI v2.0 - Complete Testing Checklist

## ✅ Pre-Testing Setup

### 1. Backend Setup
```powershell
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod
.\venv\Scripts\activate
python init_db.py
python seed_quiz.py
python -m uvicorn app.main:app --reload
```

**Expected**: Backend running on http://localhost:8000

### 2. Frontend Setup
```powershell
cd c:\Users\srushti kadam\OneDrive\Desktop\pcod\frontend
npm run dev
```

**Expected**: Frontend running on http://localhost:3000

---

## 🧪 Testing Checklist

### Backend API Tests

#### Health Check
- [ ] Visit: http://localhost:8000/health
- [ ] Expected: `{"status": "healthy"}`

#### API Documentation
- [ ] Visit: http://localhost:8000/docs
- [ ] Expected: Swagger UI with all endpoints visible

#### Test Endpoints (using Swagger or curl)
- [ ] POST /api/v1/assess - Submit assessment
- [ ] GET /api/v1/health-score/{user_id} - Get health score
- [ ] POST /api/v1/period/add - Add period log
- [ ] GET /api/v1/period/history/{user_id} - Get period history
- [ ] GET /api/v1/period/prediction/{user_id} - Get prediction
- [ ] POST /api/v1/mental-health/add - Add mental health log
- [ ] GET /api/v1/mental-health/history/{user_id} - Get history
- [ ] GET /api/v1/mental-health/insights/{user_id} - Get insights
- [ ] GET /api/v1/diet-plan/{user_id} - Get diet plan
- [ ] GET /api/v1/quiz/questions - Get quiz questions
- [ ] POST /api/v1/quiz/submit - Submit quiz
- [ ] GET /api/v1/report/monthly/{user_id} - Get monthly report

---

### Frontend Tests

#### 1. Landing Page (/)
- [ ] Page loads without errors
- [ ] "Get Started" button visible
- [ ] Click "Get Started" → redirects to /dashboard/home

#### 2. Dashboard Home (/dashboard/home)
- [ ] Sidebar visible with 7 tabs
- [ ] Health score widget displays (may show 0 initially)
- [ ] Quick stats cards visible
- [ ] Quick action buttons work

#### 3. Assessment Tab (/dashboard/assessment)
- [ ] "Start Assessment" button visible
- [ ] Click button → redirects to /assessment
- [ ] Feature cards display correctly

#### 4. Period Tracker Tab (/dashboard/period)
- [ ] Period log form displays
- [ ] Can select dates
- [ ] Can adjust pain level slider
- [ ] Submit form → shows success toast
- [ ] Period history displays after adding log
- [ ] Prediction card shows message

#### 5. Mental Health Tab (/dashboard/mental-health)
- [ ] Daily check-in form displays
- [ ] All sliders work (stress, sleep, energy)
- [ ] Mood dropdown works
- [ ] Submit form → shows success toast
- [ ] Averages display after adding logs
- [ ] AI insights appear after multiple logs

#### 6. Diet Plan Tab (/dashboard/diet)
- [ ] Shows message to complete assessment (if no assessment)
- [ ] After assessment: Foods to eat/avoid display
- [ ] Weekly meal plan with day selector works
- [ ] Nutritional tips display

#### 7. Quiz Tab (/dashboard/quiz)
- [ ] Quiz questions load
- [ ] Can select answers
- [ ] Progress bar updates
- [ ] Previous/Next buttons work
- [ ] Submit quiz → shows results
- [ ] Score and awareness level display
- [ ] Health tips display

#### 8. Reports Tab (/dashboard/reports)
- [ ] Monthly summary displays
- [ ] Health score trend shows
- [ ] Trend indicators work
- [ ] Achievements list displays
- [ ] Recommendations display

---

## 🔧 Common Issues & Fixes

### Issue: "Cannot read properties of null"
**Fix**: Refresh page, check if backend is running

### Issue: "Failed to fetch"
**Fix**: Ensure backend is running on port 8000

### Issue: "No quiz questions available"
**Fix**: Run `python seed_quiz.py` in backend

### Issue: "Module not found"
**Fix**: Run `npm install` in frontend directory

### Issue: Health score shows 0
**Fix**: Complete an assessment first, then check period/mental health logs

---

## 📊 Success Criteria

✅ All 7 dashboard tabs load without errors
✅ Forms submit successfully with toast notifications
✅ Data persists across page refreshes
✅ Navigation between tabs works smoothly
✅ No console errors in browser DevTools
✅ Backend responds to all API calls
✅ Quiz can be completed and scored
✅ Period predictions work after 2+ logs

---

## 🎯 Full User Flow Test

1. **Start** → Visit http://localhost:3000
2. **Landing** → Click "Get Started"
3. **Dashboard Home** → View health score
4. **Assessment** → Complete PCOS assessment
5. **Period Tracker** → Add 2-3 period logs
6. **Mental Health** → Add daily check-ins
7. **Diet Plan** → View personalized recommendations
8. **Quiz** → Complete all questions
9. **Reports** → View monthly progress
10. **Verify** → All data persists, no errors

---

## 📝 Notes

- User ID is stored in localStorage
- First-time users will see empty states
- Data accumulates with usage
- Backend must be running for all features
- Quiz requires seed_quiz.py to be run

---

**Status**: Ready for Testing ✅
**Version**: 2.0.0
**Last Updated**: 2026-02-16
