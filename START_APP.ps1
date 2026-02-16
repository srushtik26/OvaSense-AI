# OvaSense AI v2.0 - Quick Start Script
# Run this to start both backend and frontend

Write-Host "🚀 Starting OvaSense AI v2.0..." -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
Write-Host "📡 Checking backend status..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend is already running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend is not running. Please start it first:" -ForegroundColor Red
    Write-Host ""
    Write-Host "   cd c:\Users\srushti kadam\OneDrive\Desktop\pcod" -ForegroundColor White
    Write-Host "   .\venv\Scripts\activate" -ForegroundColor White
    Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Start frontend
Write-Host ""
Write-Host "🎨 Starting frontend..." -ForegroundColor Yellow
Set-Location "c:\Users\srushti kadam\OneDrive\Desktop\pcod\frontend"
npm run dev
