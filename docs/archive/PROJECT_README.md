# Wikipedia Quiz Application - Implementation

This directory contains the complete implementation of the Wikipedia Quiz Application as specified in the PRD and ADRs.

## 📁 Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agents/         # LangGraph agent pipeline
│   │   │   └── quiz_generator.py
│   │   ├── api/            # API endpoints
│   │   │   └── quiz.py
│   │   ├── models/         # Pydantic models
│   │   │   └── quiz.py
│   │   ├── services/       # External services
│   │   │   └── wikipedia_client.py
│   │   ├── utils/          # Utilities
│   │   │   └── cache.py
│   │   └── main.py         # Application entry
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   ├── types/          # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
└── Dockerfile             # Production deployment
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Azure OpenAI API access with a deployed model

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Azure OpenAI configuration:
# - AZURE_OPENAI_ENDPOINT (e.g., https://xxx.openai.azure.com/)
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_API_VERSION (e.g., 2024-02-15-preview)
# - AZURE_OPENAI_DEPLOYMENT_NAME (your deployed model name)
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Run Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m app.main
```
Runs at http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Runs at http://localhost:5173

**Access the app:** Open http://localhost:5173 in your browser

## 🎯 How It Works

### User Flow

1. **Enter Topic**: User inputs any Wikipedia topic (e.g., "Solar System")
2. **Choose Questions**: Select 3-20 questions
3. **Generate**: AI creates quiz in ~5-10 seconds
4. **Take Quiz**: Answer multiple-choice questions
5. **View Results**: Get instant feedback with explanations

### Technical Architecture

#### Backend (FastAPI)
- **API Endpoints**: `/api/quiz/generate`, `/api/quiz/submit`, `/api/health`
- **Agent Pipeline** (LangGraph):
  1. Topic Resolution - Find Wikipedia article
  2. Content Extraction - Get article content
  3. Question Generation - Claude creates questions
  4. Quality Validation - Verify and structure
- **Caching**: In-memory with TTL (7 days for Wikipedia, 24h for quizzes)

#### Frontend (React + TypeScript)
- **QuizForm**: Topic and question count input
- **QuizDisplay**: Interactive quiz-taking interface
- **ResultsDisplay**: Score and detailed feedback

## 🔧 API Reference

### POST /api/quiz/generate
Generate a new quiz.

**Request:**
```json
{
  "topic": "Solar System",
  "num_questions": 10
}
```

**Response:**
```json
{
  "quiz_id": "uuid",
  "topic": "Solar System",
  "questions": [
    {
      "question_id": "uuid",
      "text": "What is the largest planet?",
      "options": [
        {"id": "A", "text": "Earth"},
        {"id": "B", "text": "Jupiter"},
        {"id": "C", "text": "Mars"},
        {"id": "D", "text": "Venus"}
      ],
      "correct_answer_id": "B"
    }
  ],
  "generated_at": "2025-12-11T..."
}
```

### POST /api/quiz/submit
Submit quiz answers.

**Request:**
```json
{
  "quiz_id": "uuid",
  "answers": [
    {
      "question_id": "uuid",
      "selected_answer_id": "B"
    }
  ]
}
```

**Response:**
```json
{
  "quiz_id": "uuid",
  "score": {
    "correct": 8,
    "total": 10,
    "percentage": 80.0
  },
  "results": [...],
  "submitted_at": "2025-12-11T..."
}
```

## 🐳 Docker Deployment

```bash
# Build
docker build -t wikipedia-quiz .

# Run
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  wikipedia-quiz
```

Access at http://localhost:8000

## 📊 Performance

- Quiz generation: 5-10 seconds (includes AI processing)
- Cached responses: <100ms
- Quiz submission: <200ms

## 🧪 Testing

Try these sample topics:
- Solar System
- World War II
- Leonardo da Vinci
- Quantum mechanics
- Ancient Egypt
- Python (programming language)

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| ANTHROPIC_API_KEY | Yes | Your Anthropic API key for Claude |

## 📝 Implementation Notes

This implementation follows the specifications in:
- **PRD**: `specs/prd.md`
- **ADRs**: `specs/adr/001-004`
- **Implementation Plan**: `specs/IMPLEMENTATION_PLAN.md`

**Key Features Implemented:**
✅ React + Vite frontend
✅ FastAPI backend
✅ LangGraph agent pipeline (4 stages)
✅ Claude 3.5 Sonnet integration
✅ Wikipedia API integration
✅ In-memory caching with TTL
✅ Responsive UI
✅ Error handling
✅ Docker deployment

## 🐛 Troubleshooting

**Quiz generation fails:**
- Check ANTHROPIC_API_KEY is set correctly
- Verify topic exists on Wikipedia
- Check backend logs for detailed errors

**Frontend can't connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify Vite proxy configuration in `frontend/vite.config.ts`

**Build errors:**
- Frontend: Run `npm install` in frontend directory
- Backend: Ensure Python 3.11+ and run `pip install -r requirements.txt`

## 📄 License

See LICENSE.md
