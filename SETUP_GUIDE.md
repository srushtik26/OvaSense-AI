# Complete Setup Guide - OvaSense AI

This guide will walk you through setting up the entire project, including the database.

## Prerequisites

Before starting, ensure you have:
- ✅ Python 3.9 or higher installed
- ✅ Node.js 18 or higher installed
- ✅ PostgreSQL 12 or higher installed
- ✅ Git (optional, for version control)

## Step 1: Install PostgreSQL

### Windows:
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Default port is 5432 (keep this unless you change it)

### macOS:
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 2: Create PostgreSQL Database

### Option A: Using psql (Command Line)

1. Open terminal/command prompt
2. Connect to PostgreSQL:
   ```bash
   # Windows (if PostgreSQL bin is in PATH)
   psql -U postgres
   
   # Or on macOS/Linux
   sudo -u postgres psql
   ```

3. Create the database:
   ```sql
   CREATE DATABASE ovasense_db;
   ```

4. Create a user (optional, but recommended):
   ```sql
   CREATE USER ovasense_user WITH PASSWORD 'your_password_here';
   GRANT ALL PRIVILEGES ON DATABASE ovasense_db TO ovasense_user;
   ```

5. Exit psql:
   ```sql
   \q
   ```

### Option B: Using pgAdmin (GUI)

1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Name: `ovasense_db`
4. Click "Save"

## Step 3: Set Up Backend

### 3.1 Navigate to Project Directory

```bash
cd "C:\Users\srushti kadam\OneDrive\Desktop\pcod"
```

### 3.2 Create Virtual Environment

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### 3.3 Activate Virtual Environment

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3.4 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- SQLAlchemy
- PostgreSQL driver (psycopg2)
- Machine learning libraries
- And all other dependencies

### 3.5 Create Environment File

Create a file named `.env` in the root directory (same level as `requirements.txt`):

**Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**macOS/Linux:**
```bash
touch .env
```

Then open `.env` and add:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ovasense_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important:** Replace:
- `your_password` with your PostgreSQL password
- `postgres` with your PostgreSQL username (if different)
- `your-secret-key-change-this-in-production` with a random string

**Example:**
```env
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/ovasense_db
SECRET_KEY=super-secret-key-12345-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3.6 Test Database Connection

Create a test file `test_db.py`:

```python
from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

Run it:
```bash
python test_db.py
```

If successful, you'll see: `✅ Database connection successful!`

### 3.7 Initialize Database Tables

The tables will be created automatically when you first run the FastAPI server. But you can also create them manually:

```python
# Create init_db.py
from app.database import engine, Base
from app import models

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")
```

Run:
```bash
python init_db.py
```

## Step 4: Run Backend Server

### Option A: Using the provided script

**Windows:**
```bash
run_backend.bat
```

**macOS/Linux:**
```bash
chmod +x run_backend.sh
./run_backend.sh
```

### Option B: Direct command

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4.1 Verify Backend is Running

1. Open browser: http://localhost:8000
   - Should show: `{"message":"OvaSense AI API","version":"1.0.0","status":"operational"}`

2. Check API docs: http://localhost:8000/docs
   - Should show Swagger UI with all endpoints

3. Health check: http://localhost:8000/health
   - Should show: `{"status":"healthy"}`

## Step 5: Set Up Frontend

### 5.1 Navigate to Frontend Directory

Open a **new terminal window** (keep backend running in the first one):

```bash
cd "C:\Users\srushti kadam\OneDrive\Desktop\pcod\frontend"
```

### 5.2 Install Node Dependencies

```bash
npm install
```

This will install:
- Next.js
- React
- TypeScript
- Tailwind CSS
- And all other frontend dependencies

### 5.3 Run Frontend Development Server

```bash
npm run dev
```

You should see:
```
  ▲ Next.js 14.0.3
  - Local:        http://localhost:3000
  - ready started server on 0.0.0.0:3000
```

## Step 6: Test the Application

1. **Open browser**: http://localhost:3000
   - You should see the OvaSense AI welcome page

2. **Click "Start Assessment"**

3. **Fill out the questionnaire** (5 steps):
   - Personal Details
   - Menstrual Health
   - Symptoms
   - Metabolic Factors
   - Lifestyle

4. **Submit and view results**

5. **Download PDF report**

## Troubleshooting

### Database Connection Issues

**Error: "could not connect to server"**
- ✅ Check PostgreSQL is running:
  ```bash
  # Windows
  services.msc  # Look for "postgresql" service
  
  # macOS/Linux
  sudo systemctl status postgresql
  ```

**Error: "password authentication failed"**
- ✅ Check your `.env` file has correct password
- ✅ Verify username is correct (usually `postgres`)

**Error: "database does not exist"**
- ✅ Create the database: `CREATE DATABASE ovasense_db;`

**Error: "relation does not exist"**
- ✅ Run the init script to create tables:
  ```bash
  python init_db.py
  ```

### Port Already in Use

**Error: "Address already in use"**

**Backend (port 8000):**
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

**Frontend (port 3000):**
```bash
# Or use a different port
npm run dev -- -p 3001
```

### Module Not Found Errors

**Error: "No module named 'app'"**
- ✅ Make sure you're in the project root directory
- ✅ Virtual environment is activated
- ✅ Dependencies are installed: `pip install -r requirements.txt`

**Error: "Cannot find module" (Node.js)**
- ✅ Navigate to frontend directory: `cd frontend`
- ✅ Install dependencies: `npm install`

### Frontend Can't Connect to Backend

**Error: "Network Error" or "Connection refused"**
- ✅ Check backend is running on http://localhost:8000
- ✅ Check `frontend/next.config.js` has correct API URL
- ✅ Try accessing API directly: http://localhost:8000/api/v1/assessments/analyze

## Quick Test Script

After setup, test the API:

```bash
# Make sure backend is running first
python test_api.py
```

This will test:
- Health endpoint
- Assessment submission
- Results retrieval

## Project Structure Summary

```
pcod/
├── app/                    # Backend code
│   ├── api/               # API endpoints
│   ├── services/          # Business logic
│   ├── models.py          # Database models
│   └── main.py            # FastAPI app
├── frontend/              # Frontend code
│   └── app/               # Next.js pages
├── .env                   # Environment variables (CREATE THIS!)
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## Next Steps

1. ✅ Database is set up and connected
2. ✅ Backend is running on port 8000
3. ✅ Frontend is running on port 3000
4. ✅ Test the application flow
5. ✅ Review the API documentation at http://localhost:8000/docs

## Production Deployment Notes

For production:
- Use environment-specific `.env` files
- Set strong `SECRET_KEY`
- Use production database (not localhost)
- Enable HTTPS
- Configure CORS properly
- Use production ASGI server (Gunicorn)
- Set up proper logging
- Implement rate limiting
- Add authentication/authorization

---

**Need Help?** Check the error messages carefully - they usually point to the issue!

