@echo off
REM Script to run the FastAPI backend on Windows

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

