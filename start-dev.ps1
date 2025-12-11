# Wikipedia Quiz Application - Development Server Launcher
# This script starts both backend and frontend servers

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host " Wikipedia Quiz Application - Starting Development Servers" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# Check if backend .env exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  Warning: backend\.env not found!" -ForegroundColor Yellow
    Write-Host "Please create backend\.env with your ANTHROPIC_API_KEY" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# Start backend in new window
Write-Host "🚀 Starting backend server..." -ForegroundColor Green
$backendScript = @"
Set-Location '$PWD\backend'
.\venv\Scripts\activate
Write-Host 'Backend running on http://localhost:8000' -ForegroundColor Green
Write-Host 'API docs at http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host ''
python -m app.main
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait for backend to initialize
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 4

# Start frontend in new window  
Write-Host "🚀 Starting frontend server..." -ForegroundColor Green
$frontendScript = @"
Set-Location '$PWD\frontend'
Write-Host 'Frontend running on http://localhost:5173' -ForegroundColor Green
Write-Host ''
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host ""
Write-Host "✅ Development servers started!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open the application in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Servers are running in separate windows." -ForegroundColor Green
Write-Host "Close those windows to stop the servers." -ForegroundColor Yellow
