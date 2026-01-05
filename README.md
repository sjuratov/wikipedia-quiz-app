# Wikipedia Quiz Application

AI-powered quiz generator that creates custom multiple-choice quizzes from Wikipedia articles using Azure OpenAI.

## ✨ Features

- **🎯 Any Topic**: Generate quizzes on virtually any Wikipedia topic
- **🤖 AI-Powered**: Intelligent question generation using Azure OpenAI
- **📊 Customizable**: Choose number of questions (3-20)
- **✅ Instant Feedback**: Immediate results with detailed explanations
- **🔗 Source Verification**: Direct links to Wikipedia sources for each answer
- **💾 Smart Caching**: Reduced API calls with intelligent caching
- **📱 Responsive**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Azure OpenAI API access (endpoint, API key, deployment name)

### Setup (First Time)

```powershell
# Run automated setup script
.\setup.ps1

# Configure your Azure OpenAI credentials
# Edit backend\.env and add:
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_API_VERSION
# - AZURE_OPENAI_DEPLOYMENT_NAME

# Start development servers
.\start-dev.ps1
```

Open http://localhost:5173 in your browser 🎉

### Daily Development

```powershell
# Start both backend and frontend servers
.\start-dev.ps1
```

## 📖 Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation and troubleshooting
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Commands, URLs, and daily workflows
- **[Integration Guide](docs/INTEGRATION.md)** - Spec2cloud integration details
- **[Specifications](specs/)** - Product requirements and technical documentation

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python)
- Azure OpenAI (GPT-4)
- LangGraph (Agent pipeline)
- Wikipedia API

**Frontend:**
- React + TypeScript
- Vite
- Modern CSS

**Deployment:**
- Docker
- Azure (optional)

### Project Structure

```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── agents/      # LangGraph quiz generation pipeline
│   │   ├── api/         # REST API endpoints
│   │   ├── models/      # Pydantic data models
│   │   ├── services/    # Wikipedia client
│   │   └── utils/       # Caching utilities
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json
├── specs/               # Product & technical specs
│   ├── prd.md          # Product requirements
│   ├── features/       # Feature specifications
│   └── adr/            # Architecture decisions
└── docs/               # Documentation
```

## 🎮 How It Works

1. **User Input**: Enter any Wikipedia topic and select number of questions
2. **Content Retrieval**: System fetches Wikipedia article via API
3. **AI Generation**: Azure OpenAI generates intelligent multiple-choice questions
4. **Quality Validation**: Questions validated for clarity and accuracy
5. **Interactive Quiz**: User answers questions in clean interface
6. **Instant Results**: Immediate feedback with score and answer verification links

## 🔧 Development

### Backend

```powershell
cd backend
.\venv\Scripts\activate
python -m app.main

# API docs: http://localhost:8000/docs
```

### Frontend

```powershell
cd frontend
npm run dev

# App: http://localhost:5173
```

### Testing

```powershell
# Backend tests
cd backend
.\venv\Scripts\activate
python test_backend.py

# Manual API test
curl http://localhost:8000/api/health
```

## 🌐 API Endpoints

- `POST /api/quiz/generate` - Generate a new quiz
- `POST /api/quiz/submit` - Submit answers and get results
- `GET /api/health` - Health check

See full API documentation at http://localhost:8000/docs

## 📦 Built with Spec2Cloud

This project was built using the **[Spec2Cloud framework](SPEC2CLOUD_FRAMEWORK.md)** - an AI-powered development workflow that transforms product ideas into production-ready applications using specialized GitHub Copilot agents.

The framework orchestrates:
- **PM Agent** - Product requirements and feature specs
- **Dev Lead Agent** - Technical review and standards
- **Dev Agent** - Implementation and coding
- **Azure Agent** - Cloud deployment and IaC

Learn more in [SPEC2CLOUD_FRAMEWORK.md](SPEC2CLOUD_FRAMEWORK.md).

## 📝 License

MIT License - See [LICENSE.md](LICENSE.md)

## 🤝 Contributing

Contributions welcome! This project demonstrates the Spec2Cloud workflow for building AI-powered applications.

---

**Generate quizzes on any topic in seconds!** 🚀
