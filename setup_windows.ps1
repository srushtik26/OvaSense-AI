# OvaSense AI - Windows Setup Script
# Run this script in PowerShell to set up the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OvaSense AI - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✅ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PostgreSQL not found in PATH" -ForegroundColor Yellow
    Write-Host "   Make sure PostgreSQL is installed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 1: Setting up Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Check for .env file
Write-Host ""
Write-Host "Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create .env file with:" -ForegroundColor Yellow
    Write-Host "DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ovasense_db" -ForegroundColor White
    Write-Host "SECRET_KEY=your-secret-key-here" -ForegroundColor White
    Write-Host "ALGORITHM=HS256" -ForegroundColor White
    Write-Host "ACCESS_TOKEN_EXPIRE_MINUTES=30" -ForegroundColor White
    Write-Host ""
    $createEnv = Read-Host "Would you like to create .env file now? (y/n)"
    if ($createEnv -eq "y") {
        $dbPassword = Read-Host "Enter PostgreSQL password" -AsSecureString
        $dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))
        $secretKey = Read-Host "Enter secret key (or press Enter for default)"
        if ([string]::IsNullOrWhiteSpace($secretKey)) {
            $secretKey = "dev-secret-key-change-in-production"
        }
        @"
DATABASE_URL=postgresql://postgres:$dbPasswordPlain@localhost:5432/ovasense_db
SECRET_KEY=$secretKey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"@ | Out-File -FilePath ".env" -Encoding utf8
        Write-Host "✅ .env file created" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 2: Setting up Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend
if (Test-Path "frontend") {
    Set-Location frontend
    
    # Install Node dependencies
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes..." -ForegroundColor Yellow
    npm install
    Write-Host "✅ Node.js dependencies installed" -ForegroundColor Green
    
    Set-Location ..
} else {
    Write-Host "⚠️  Frontend directory not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Make sure PostgreSQL is running" -ForegroundColor White
Write-Host "2. Create database: CREATE DATABASE ovasense_db;" -ForegroundColor White
Write-Host "3. Test database: python test_db.py" -ForegroundColor White
Write-Host "4. Initialize tables: python init_db.py" -ForegroundColor White
Write-Host "5. Start backend: uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "6. Start frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see START_HERE.md" -ForegroundColor Cyan

