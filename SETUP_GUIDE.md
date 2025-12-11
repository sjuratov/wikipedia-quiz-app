# Development Setup and Installation Guide

This guide will help you set up and run the Wikipedia Quiz Application locally.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.11 or higher**
   - Check: `python --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 18 or higher**
   - Check: `node --version`
   - Download: https://nodejs.org/

3. **Azure OpenAI Access**
   - You need an Azure subscription with OpenAI service deployed
   - Obtain: Endpoint URL, API Key, API Version, and Deployment Name
   - Learn more: https://learn.microsoft.com/azure/ai-services/openai/

## Step-by-Step Setup

### 1. Install Backend Dependencies

```powershell
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```powershell
# Still in backend directory
# Copy the example env file
copy .env.example .env

# Open .env in your editor and add your Azure OpenAI configuration:
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your_api_key_here
# AZURE_OPENAI_API_VERSION=2024-02-15-preview
# AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

### 3. Install Frontend Dependencies

```powershell
# Navigate to frontend directory (from project root)
cd ..\frontend

# Install npm packages
npm install
```

### 4. Start the Development Servers

You'll need two terminal windows:

**Terminal 1 - Backend Server:**
```powershell
cd backend
.\venv\Scripts\activate
python -m app.main
```

You should see:
```
🚀 Starting Wikipedia Quiz Application...
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend Server:**
```powershell
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.8  ready in xxx ms

➜  Local:   http://localhost:5173/
```

### 5. Access the Application

Open your web browser and go to: **http://localhost:5173**

You should see the Wikipedia Quiz application home page!

## Verification

Test that everything works:

1. **Backend Health Check**
   - Open: http://localhost:8000/api/health
   - Should see: `{"status":"healthy","services":{...}}`

2. **Generate a Quiz**
   - In the app, enter topic: "Solar System"
   - Select: 5 questions
   - Click "Generate Quiz"
   - Wait 5-10 seconds for AI to generate questions

3. **Take the Quiz**
   - Answer the questions
   - Click "Submit Quiz"
   - View your results

## Common Issues

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Ensure virtual environment is activated and dependencies installed:
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: `ValueError: ANTHROPIC_API_KEY environment variable not set`
**Solution**: Check your `.env` file exists and contains valid API key:
```powershell
cd backend
type .env
# Should show: ANTHROPIC_API_KEY=sk-ant-...
```

**Problem**: Port 8000 already in use
**Solution**: Kill the process or use a different port:
```powershell
# Find process on port 8000
netstat -ano | findstr :8000
# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Frontend Issues

**Problem**: `npm: command not found`
**Solution**: Install Node.js from https://nodejs.org/

**Problem**: Port 5173 already in use
**Solution**: Vite will automatically try the next available port (5174, 5175, etc.)

**Problem**: Cannot connect to backend (CORS errors)
**Solution**: Ensure:
1. Backend is running on port 8000
2. Frontend dev server is using the proxy configuration
3. Check `frontend/vite.config.ts` has correct proxy settings

### API Issues

**Problem**: Quiz generation fails with "topic_not_found"
**Solution**: Try a different, more common Wikipedia topic (e.g., "Python (programming language)")

**Problem**: Rate limit errors
**Solution**: Wait a few moments between requests. The app includes caching to reduce API calls.

## Development Workflow

### Making Changes

**Backend Changes:**
- FastAPI auto-reloads on file changes
- Check terminal for any errors
- Test endpoints at http://localhost:8000/docs

**Frontend Changes:**
- Vite auto-reloads on file changes
- Check browser console for errors
- Changes reflect immediately in browser

### Building for Production

**Build Frontend:**
```powershell
cd frontend
npm run build
```
Outputs to `frontend/dist/`

**Run Production Build:**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Access at: http://localhost:8000

## Next Steps

- Review the code in `backend/app/` and `frontend/src/`
- Check `PROJECT_README.md` for architecture details
- Read the specifications in `specs/` directory
- Try modifying questions or adding features

## Getting Help

If you encounter issues:

1. Check the terminal output for error messages
2. Review the troubleshooting section above
3. Ensure all prerequisites are properly installed
4. Verify your API key is valid and has credits

## Environment Variables Reference

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| ANTHROPIC_API_KEY | backend/.env | Yes | Your Anthropic API key for Claude |

## Useful Commands

```powershell
# Backend
cd backend
.\venv\Scripts\activate          # Activate virtual environment
python -m app.main               # Run backend
pip list                         # Show installed packages
deactivate                       # Deactivate virtual environment

# Frontend
cd frontend
npm run dev                      # Development server
npm run build                    # Production build
npm run preview                  # Preview production build

# Both
# Ctrl+C to stop servers
```
