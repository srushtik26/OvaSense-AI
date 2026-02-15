# OvaSense AI - Setup Guide

## Quick Start

### 1. Backend Setup

#### Step 1: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Database Setup

1. Install PostgreSQL if not already installed
2. Create a database:
```bash
createdb ovasense_db
```

3. Create `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ovasense_db
SECRET_KEY=your-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `username` and `password` with your PostgreSQL credentials.

#### Step 3: Run Backend

```bash
# On Windows
run_backend.bat

# On macOS/Linux
chmod +x run_backend.sh
./run_backend.sh

# Or directly:
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 2. Frontend Setup

#### Step 1: Install Node Dependencies

```bash
cd frontend
npm install
```

#### Step 2: Run Frontend

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Testing the System

1. Open `http://localhost:3000` in your browser
2. Click "Start Assessment"
3. Fill out the questionnaire (all 5 steps)
4. Submit and view your results
5. Download the PDF report

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running
- Check your `.env` file has correct database credentials
- Verify the database exists: `psql -l | grep ovasense_db`

### Port Already in Use

If port 8000 is in use:
```bash
uvicorn app.main:app --reload --port 8001
```

Then update `frontend/next.config.js` to point to the new port.

### Module Not Found Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### Frontend Build Issues

- Clear Next.js cache: `rm -rf frontend/.next`
- Reinstall node modules: `rm -rf frontend/node_modules && npm install`

## Production Deployment

### Backend

1. Use a production ASGI server:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Set up environment variables properly
3. Use a production database (not SQLite)
4. Enable HTTPS

### Frontend

1. Build for production:
```bash
cd frontend
npm run build
npm start
```

2. Update API endpoint in `next.config.js` to point to production backend

## Environment Variables

Required environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens (if implementing auth)
- `ALGORITHM`: JWT algorithm (default: HS256)

## Database Migrations

The system uses SQLAlchemy with automatic table creation. For production, consider using Alembic for migrations:

```bash
pip install alembic
alembic init alembic
# Configure alembic.ini with your database URL
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Security Notes

- Never commit `.env` file to version control
- Use strong `SECRET_KEY` in production
- Enable CORS properly for production (update `app/main.py`)
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Add authentication if storing user data

