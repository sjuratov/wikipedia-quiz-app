# Wikipedia Quiz Application - First Time Setup
# Run this script once to set up your development environment

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host " Wikipedia Quiz Application - First Time Setup" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "🔍 Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.11+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green

# Check Node
Write-Host "🔍 Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Node.js not found! Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Found: Node.js $nodeVersion" -ForegroundColor Green
Write-Host ""

# Setup Backend
Write-Host "🔧 Setting up backend..." -ForegroundColor Cyan
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  ✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate and install dependencies
Write-Host "  Installing Python dependencies..." -ForegroundColor Yellow
.\venv\Scripts\activate
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Python dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "  Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "  ✅ .env file created" -ForegroundColor Green
    Write-Host "  ⚠️  YOU MUST EDIT backend\.env AND ADD YOUR ANTHROPIC_API_KEY!" -ForegroundColor Yellow
    $needsKey = $true
} else {
    Write-Host "  ✅ .env file already exists" -ForegroundColor Green
    $content = Get-Content ".env" -Raw
    if ($content -match "your_anthropic_api_key_here" -or $content -match "ANTHROPIC_API_KEY=$") {
        Write-Host "  ⚠️  .env file exists but API key looks incomplete" -ForegroundColor Yellow
        $needsKey = $true
    }
}

Write-Host "✅ Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Setup Frontend
Set-Location ..\frontend
Write-Host "🔧 Setting up frontend..." -ForegroundColor Cyan

# Install npm dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing npm dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install npm dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✅ npm dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✅ npm dependencies already installed" -ForegroundColor Green
}

Write-Host "✅ Frontend setup complete!" -ForegroundColor Green
Write-Host ""

Set-Location ..

# Final summary
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host " ✅ Setup Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host ""

if ($needsKey) {
    Write-Host "⚠️  IMPORTANT: Next Steps" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Get your Anthropic API key:" -ForegroundColor White
    Write-Host "   - Go to https://console.anthropic.com/" -ForegroundColor Cyan
    Write-Host "   - Sign up or log in" -ForegroundColor Cyan
    Write-Host "   - Create a new API key" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Edit backend\.env file:" -ForegroundColor White
    Write-Host "   - Open backend\.env in your text editor" -ForegroundColor Cyan
    Write-Host "   - Replace 'your_anthropic_api_key_here' with your actual key" -ForegroundColor Cyan
    Write-Host "   - Save the file" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. Start the application:" -ForegroundColor White
    Write-Host "   .\start-dev.ps1" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "🚀 You're ready to go!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Start the development servers:" -ForegroundColor White
    Write-Host "  .\start-dev.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or test the backend:" -ForegroundColor White
    Write-Host "  cd backend" -ForegroundColor Cyan
    Write-Host "  .\venv\Scripts\activate" -ForegroundColor Cyan
    Write-Host "  python test_backend.py" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "📚 Documentation:" -ForegroundColor White
Write-Host "  SETUP_GUIDE.md       - Detailed setup instructions" -ForegroundColor Cyan
Write-Host "  PROJECT_README.md    - Technical documentation" -ForegroundColor Cyan
Write-Host "  SCRIPTS_GUIDE.md     - Helper scripts reference" -ForegroundColor Cyan
Write-Host ""
