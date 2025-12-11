# Wikipedia Quiz Application - Quick Reference

## 🚀 Quick Start (First Time)

```powershell
# 1. Run setup script
.\setup.ps1

# 2. Add your Azure OpenAI details to backend\.env
# - AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
# - AZURE_OPENAI_API_KEY=your_key
# - AZURE_OPENAI_API_VERSION=2024-02-15-preview
# - AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment

# 3. Start development servers
.\start-dev.ps1

# 4. Open http://localhost:5173
```

## 📋 Daily Development

### Start Servers
```powershell
.\start-dev.ps1
```

### Manual Start (2 terminals)
```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python -m app.main

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## 🔧 Useful Commands

### Backend
```powershell
cd backend
.\venv\Scripts\activate

# Run server
python -m app.main

# Test backend
python test_backend.py

# Install new package
pip install package_name
pip freeze > requirements.txt

# Check API docs
# http://localhost:8000/docs
```

### Frontend
```powershell
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new package
npm install package_name
```

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application |
| Backend API | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/api/health | Backend health status |

## 📁 Key Files

### Backend
| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI application |
| `backend/app/agents/quiz_generator.py` | LangGraph agent pipeline |
| `backend/app/api/quiz.py` | API endpoints |
| `backend/app/models/quiz.py` | Data models |
| `backend/app/services/wikipedia_client.py` | Wikipedia API client |
| `backend/app/utils/cache.py` | Caching logic |
| `backend/.env` | Environment variables (API key) |
| `backend/requirements.txt` | Python dependencies |

### Frontend
| File | Purpose |
|------|---------|
| `frontend/src/App.tsx` | Main application component |
| `frontend/src/components/QuizForm.tsx` | Quiz creation form |
| `frontend/src/components/QuizDisplay.tsx` | Quiz taking interface |
| `frontend/src/components/ResultsDisplay.tsx` | Results display |
| `frontend/src/services/api.ts` | API client |
| `frontend/src/types/quiz.ts` | TypeScript types |
| `frontend/vite.config.ts` | Vite configuration |
| `frontend/package.json` | npm dependencies |

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check virtual environment
cd backend
.\venv\Scripts\activate
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt

# Check .env file
type .env  # Should have ANTHROPIC_API_KEY
```

### Frontend won't start
```powershell
# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Quiz generation fails
- Check ANTHROPIC_API_KEY in `backend/.env`
- Verify you have API credits
- Try a different topic (e.g., "Python programming language")
- Check backend terminal for errors

### Port already in use
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

## 🧪 Testing

### Test Backend
```powershell
cd backend
.\venv\Scripts\activate
python test_backend.py
```

### Manual API Testing
```powershell
# Health check
curl http://localhost:8000/api/health

# Generate quiz
curl -X POST http://localhost:8000/api/quiz/generate `
  -H "Content-Type: application/json" `
  -d '{\"topic\":\"Solar System\",\"num_questions\":5}'
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `PROJECT_README.md` | Technical overview and architecture |
| `SETUP_GUIDE.md` | Detailed setup instructions |
| `IMPLEMENTATION_SUMMARY.md` | Complete implementation summary |
| `SCRIPTS_GUIDE.md` | Helper scripts reference |

## 🔑 Environment Variables

Create `backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

Get your API key: https://console.anthropic.com/

## 🎯 Sample Topics

Try these topics for testing:
- Solar System
- World War II
- Leonardo da Vinci
- Python (programming language)
- Quantum mechanics
- Ancient Egypt
- Photosynthesis
- Renaissance art

## 📊 API Endpoints

### Generate Quiz
```http
POST /api/quiz/generate
Content-Type: application/json

{
  "topic": "Solar System",
  "num_questions": 10
}
```

### Submit Quiz
```http
POST /api/quiz/submit
Content-Type: application/json

{
  "quiz_id": "uuid",
  "answers": [
    {
      "question_id": "uuid",
      "selected_answer_id": "A"
    }
  ]
}
```

### Health Check
```http
GET /api/health
```

## 🔄 Project Structure

```
spec2cloud-experiment-1/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── agents/      # LangGraph pipeline
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Data models
│   │   ├── services/    # External services
│   │   ├── utils/       # Utilities
│   │   └── main.py      # App entry point
│   ├── .env             # Config (create this!)
│   └── requirements.txt # Python deps
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json     # npm deps
├── setup.ps1           # First-time setup
├── start-dev.ps1       # Start dev servers
└── README.md           # Main README
```

## 💡 Tips

1. **First time**: Run `setup.ps1` to configure everything
2. **Daily**: Use `start-dev.ps1` to launch both servers
3. **Backend changes**: Auto-reload enabled
4. **Frontend changes**: Hot module replacement enabled
5. **API testing**: Use http://localhost:8000/docs
6. **Debugging**: Check terminal output for errors
7. **Cache**: Quizzes cached for 24h, Wikipedia for 7 days

## 🆘 Getting Help

1. Check terminal output for errors
2. Review documentation in project root
3. Verify all prerequisites installed
4. Ensure API key is valid
5. Try restarting both servers

## 📝 Common Tasks

### Add New Feature
1. Backend: Add code to `backend/app/`
2. Frontend: Add code to `frontend/src/`
3. Test locally
4. Update documentation

### Change LLM Prompts
Edit `backend/app/agents/quiz_generator.py`
- Find `system_prompt` and `user_prompt`
- Modify as needed
- Restart backend to test

### Modify UI
Edit `frontend/src/App.css` for styling
Edit components in `frontend/src/components/`

### Deploy to Production
```powershell
# Build frontend
cd frontend
npm run build

# Build Docker image
docker build -t wikipedia-quiz .

# Run container
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_key wikipedia-quiz
```

## ⚡ Performance

- Quiz generation: 5-10 seconds
- Cached responses: <100ms
- Quiz submission: <200ms
- Frontend build: ~30 seconds

---

**For detailed information, see the full documentation files in the project root.**
