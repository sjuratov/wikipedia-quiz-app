# Wikipedia Quiz Application - Quick Start Scripts

## Windows PowerShell

### Setup Everything
```powershell
# Run this once to set up both backend and frontend

# Backend setup
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
@"
ANTHROPIC_API_KEY=your_key_here
"@ | Out-File -FilePath .env -Encoding utf8

Write-Host "✅ Backend setup complete!"
Write-Host "⚠️  Remember to add your ANTHROPIC_API_KEY to backend\.env"

# Frontend setup
cd ..\frontend
npm install

Write-Host "✅ Frontend setup complete!"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit backend\.env and add your Anthropic API key"
Write-Host "2. Run .\start-dev.ps1 to start both servers"
```

### Start Development Servers
```powershell
# start-dev.ps1
# Starts both backend and frontend in separate windows

# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; python -m app.main"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "✅ Development servers starting..."
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Press any key to open the app in your browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process "http://localhost:5173"
```

### Test Backend
```powershell
# test-backend.ps1
cd backend
.\venv\Scripts\activate
python test_backend.py
```

## macOS/Linux Bash

### Setup Everything
```bash
#!/bin/bash
# setup.sh

echo "Setting up Wikipedia Quiz Application..."

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_key_here
EOF

echo "✅ Backend setup complete!"
echo "⚠️  Remember to add your ANTHROPIC_API_KEY to backend/.env"

# Frontend setup
cd ../frontend
npm install

echo "✅ Frontend setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your Anthropic API key"
echo "2. Run ./start-dev.sh to start both servers"
```

### Start Development Servers
```bash
#!/bin/bash
# start-dev.sh

# Start backend in background
cd backend
source venv/bin/activate
python -m app.main &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Development servers started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
```

### Test Backend
```bash
#!/bin/bash
# test-backend.sh

cd backend
source venv/bin/activate
python test_backend.py
```

## Make Scripts Executable (Mac/Linux)

```bash
chmod +x setup.sh
chmod +x start-dev.sh
chmod +x test-backend.sh
```

## Usage

### First Time Setup

**Windows:**
```powershell
# Copy and paste the "Setup Everything" script above into PowerShell
# OR create a setup.ps1 file and run it
```

**Mac/Linux:**
```bash
./setup.sh
```

### Daily Development

**Windows:**
```powershell
# Option 1: Create start-dev.ps1 with the script above, then:
.\start-dev.ps1

# Option 2: Manual start in two terminals
# Terminal 1:
cd backend
.\venv\Scripts\activate
python -m app.main

# Terminal 2:
cd frontend
npm run dev
```

**Mac/Linux:**
```bash
# Option 1: Use script
./start-dev.sh

# Option 2: Manual start in two terminals
# Terminal 1:
cd backend
source venv/bin/activate
python -m app.main

# Terminal 2:
cd frontend
npm run dev
```

## Troubleshooting

### Backend won't start

1. Check Python version: `python --version` (need 3.11+)
2. Verify virtual environment is activated (you should see `(venv)` in prompt)
3. Check .env file exists and has valid API key
4. Look at terminal output for specific errors

### Frontend won't start

1. Check Node version: `node --version` (need 18+)
2. Delete node_modules and reinstall: `rm -rf node_modules && npm install`
3. Check if port 5173 is available

### Quiz generation fails

1. Verify ANTHROPIC_API_KEY in backend/.env
2. Check you have API credits at https://console.anthropic.com/
3. Try a different topic (e.g., "Python programming language")
4. Check backend terminal for error messages

## Environment Variables

Create `backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

Get your API key from: https://console.anthropic.com/
