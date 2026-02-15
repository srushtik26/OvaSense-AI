# Quick Start Guide - OvaSense AI

Get up and running in 5 minutes!

## Prerequisites Check

- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed  
- ✅ PostgreSQL installed and running

## Step-by-Step Setup

### 1. Backend (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
# Edit with your database credentials

# Run backend
uvicorn app.main:app --reload --port 8000
```

✅ Backend running at http://localhost:8000

### 2. Frontend (2 minutes)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

✅ Frontend running at http://localhost:3000

### 3. Test It! (1 minute)

1. Open http://localhost:3000
2. Click "Start Assessment"
3. Fill out the form
4. View results!

## Common Issues

**"Module not found"**
→ Make sure virtual environment is activated

**"Database connection error"**
→ Check your .env file and PostgreSQL is running

**"Port already in use"**
→ Change port in uvicorn command or kill the process

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [SETUP.md](SETUP.md) for detailed setup
- Review API docs at http://localhost:8000/docs

---

**Remember**: This is for informational purposes only. Always consult a healthcare professional.

