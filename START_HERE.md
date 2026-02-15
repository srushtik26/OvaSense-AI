# 🚀 START HERE - Quick Setup Guide

Follow these steps in order to get your OvaSense AI system running!

## 📋 Prerequisites Checklist

Before you start, make sure you have:
- [ ] Python 3.9+ installed (check: `python --version`)
- [ ] Node.js 18+ installed (check: `node --version`)
- [ ] PostgreSQL installed and running

---

## Step 1: Install PostgreSQL (If Not Installed)

### Windows:
1. Download from: https://www.postgresql.org/download/windows/
2. Install with default settings
3. **Remember the password** you set for `postgres` user
4. Default port: **5432**

### Verify Installation:
Open Command Prompt and type:
```bash
psql --version
```

---

## Step 2: Create Database

### Using Command Line:

1. Open Command Prompt or PowerShell
2. Connect to PostgreSQL:
   ```bash
   psql -U postgres
   ```
   (Enter your PostgreSQL password when prompted)

3. Create database:
   ```sql
   CREATE DATABASE ovasense_db;
   ```

4. Exit:
   ```sql
   \q
   ```

---

## Step 3: Set Up Backend

### 3.1 Open Terminal in Project Folder

Navigate to your project:
```bash
cd "C:\Users\srushti kadam\OneDrive\Desktop\pcod"
```

### 3.2 Create Virtual Environment

```bash
python -m venv venv
```

### 3.3 Activate Virtual Environment

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```bash
venv\Scripts\activate.bat
```

You should see `(venv)` in your prompt.

### 3.4 Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for installation to complete (may take 2-3 minutes).

### 3.5 Create .env File

**Create a file named `.env`** in the project root (same folder as `requirements.txt`).

**Content of `.env` file:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ovasense_db
SECRET_KEY=change-this-to-random-string-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANT:** Replace `YOUR_PASSWORD` with your actual PostgreSQL password!

**Example:**
```env
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/ovasense_db
SECRET_KEY=super-secret-key-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3.6 Test Database Connection

```bash
python test_db.py
```

You should see: `✅ Database connection test passed!`

If you see an error, check:
- PostgreSQL is running
- Password in `.env` is correct
- Database `ovasense_db` exists

### 3.7 Create Database Tables

```bash
python init_db.py
```

You should see: `✅ Database tables created successfully!`

### 3.8 Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

**Keep this terminal window open!** You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is now running!**

**Test it:** Open browser → http://localhost:8000

---

## Step 4: Set Up Frontend

### 4.1 Open NEW Terminal Window

**Keep the backend terminal running!** Open a new terminal window.

### 4.2 Navigate to Frontend Folder

```bash
cd "C:\Users\srushti kadam\OneDrive\Desktop\pcod\frontend"
```

### 4.3 Install Dependencies

```bash
npm install
```

Wait for installation (may take 2-3 minutes).

### 4.4 Start Frontend Server

```bash
npm run dev
```

You should see:
```
  ▲ Next.js 14.0.3
  - Local:        http://localhost:3000
```

✅ **Frontend is now running!**

---

## Step 5: Use the Application

1. **Open browser:** http://localhost:3000
2. **Click:** "Start Assessment"
3. **Fill out** the questionnaire (5 steps)
4. **Submit** and view your results
5. **Download** PDF report

---

## 🎉 Success!

You now have:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Database connected and ready

---

## 🆘 Troubleshooting

### "Module not found" error
→ Make sure virtual environment is activated (you see `(venv)` in prompt)

### "Database connection failed"
→ Check your `.env` file has correct password
→ Verify PostgreSQL is running
→ Make sure database `ovasense_db` exists

### "Port already in use"
→ Close other applications using port 8000 or 3000
→ Or use different ports

### "npm command not found"
→ Install Node.js from https://nodejs.org/

### Frontend can't connect to backend
→ Make sure backend is running on port 8000
→ Check `frontend/next.config.js` has correct API URL

---

## 📚 More Help

- **Detailed Setup:** See `SETUP_GUIDE.md`
- **Project Info:** See `README.md`
- **API Documentation:** http://localhost:8000/docs (when backend is running)

---

**Need help?** Check the error message - it usually tells you what's wrong!

