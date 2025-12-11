# ADR 004: Deployment Architecture

## Status
Accepted

## Context
The Wikipedia Quiz Application consists of three main components:
- **FastAPI Backend**: Python-based REST API serving quiz logic
- **React Frontend**: Static JavaScript SPA for user interface
- **Caching Layer**: In-memory cache (see ADR 003)

We need to determine the deployment architecture that balances simplicity, cost, and developer experience for a demo/learning application.

## Decision Drivers
- **Simplicity**: Easy to deploy and maintain
- **Developer Experience**: Quick local setup and iteration
- **Cost**: Minimal operational expenses
- **Deployment Speed**: Fast to get running
- **Learning Value**: Demonstrates practical deployment patterns
- **Scalability**: Not a priority for demo/learning use case

## Options Considered

### Option 1: Docker Compose (Self-Hosted or VM)
**Architecture:**
```yaml
services:
  backend:
    - FastAPI application
    - Port 8000
  frontend:
    - Nginx serving React build
    - Port 80/443
```

**Pros:**
- Complete local development parity with production
- Easy to understand and modify
- Full control over configuration
- Can run anywhere (local, VM, VPS)
- Good learning tool for containerization
- Low cost (can use free tier VPS)

**Cons:**
- Requires managing a server/VM
- Manual SSL certificate management
- Need to handle updates and security patches
- No built-in autoscaling or load balancing
- More operational overhead

**Cost:** $5-10/month (basic VPS)

### Option 2: Azure Container Apps
**Architecture:**
- Backend container app with ingress
- Frontend container app serving static files
- Managed container orchestration

**Pros:**
- Fully managed container platform
- Built-in HTTPS and custom domains
- Auto-scaling capabilities
- Azure integration (monitoring, logging)
- Professional deployment pattern

**Cons:**
- Higher complexity for setup
- Azure-specific knowledge required
- Higher cost for demo app
- Overkill for single-container workload
- Steeper learning curve

**Cost:** ~$20-40/month minimum

### Option 3: Vercel (Frontend) + Railway/Render (Backend)
**Architecture:**
- Vercel: Static React frontend with CDN
- Railway/Render: Containerized FastAPI backend

**Pros:**
- Excellent developer experience
- Automatic deployments from Git
- Built-in HTTPS and CDN
- Generous free tiers
- Separate scaling for frontend/backend
- Popular in modern web development

**Cons:**
- Split deployment across platforms
- Two separate configuration systems
- Potential CORS complexity
- Vendor lock-in to two platforms
- Less cohesive for learning full-stack deployment

**Cost:** Free tier or ~$5/month

### Option 4: Single Container with FastAPI Serving Static Files
**Architecture:**
```
Single Container:
  - FastAPI serves API at /api/*
  - FastAPI serves React static files at /*
  - Single port (8000)
```

**Pros:**
- Simplest possible deployment
- Single container to manage
- No CORS issues (same origin)
- Minimal configuration
- Can deploy anywhere (Render, Railway, Fly.io free tier)
- Excellent for learning and demos
- Easy local development

**Cons:**
- Frontend and backend tightly coupled
- No CDN for static files (slower global access)
- Single point of failure
- Not typical of production architectures
- Mixed concerns in one service

**Cost:** Free (generous free tiers) or ~$5/month

## Decision
**Selected: Option 4 - Single Container with FastAPI Serving Static Files**

We will deploy the application as a single Docker container where FastAPI serves both the API endpoints and the built React application.

### Implementation Approach

**Dockerfile:**
```dockerfile
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=frontend-build /app/frontend/dist ./static

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**FastAPI Configuration:**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# API routes
app.include_router(quiz_router, prefix="/api")

# Serve React static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

### Deployment Platforms
**Primary Recommendation:** Railway.app or Render.com
- Connect GitHub repository
- Automatic deployments on push
- Free tier available (sufficient for demos)
- Easy environment variable management
- Built-in HTTPS

**Alternative:** Docker Compose on any VPS (more learning value)

## Rationale

1. **Maximum Simplicity**: Single container eliminates coordination complexity between services. One deployment, one URL, one configuration file.

2. **No CORS Headaches**: Serving frontend and backend from the same origin eliminates cross-origin issues entirely.

3. **Learning Focus**: Demonstrates a practical, working deployment without overwhelming newcomers with microservices complexity.

4. **Cost Effective**: Can run on generous free tiers (Railway, Render, Fly.io) or minimal paid plans.

5. **Fast Iteration**: Single deployment target means faster development cycles and simpler CI/CD.

6. **Local Development Parity**: Same container works locally and in production.

7. **Appropriate for Scale**: For a demo/learning application with modest traffic, single container is entirely adequate.

## Consequences

### Positive
- Fastest path from code to running application
- Minimal deployment complexity
- No CORS configuration needed
- Single URL for entire application
- Easy to understand for learners
- Can deploy to multiple platforms easily
- Zero-cost deployment possible

### Negative
- Not representative of production microservices architecture
- Frontend not served via CDN (slower for global users)
- Cannot scale frontend and backend independently
- Coupled deployment (frontend change requires full redeploy)
- Less resilient (single point of failure)

### Mitigation Strategies
- Document this as a "demo architecture" in README
- Provide migration guide to separated services if needed
- Consider adding CDN in front if performance becomes issue
- Use this as learning foundation, then show evolution to microservices

## Migration Path
If the application outgrows this architecture, migration is straightforward:

### Phase 2 (Separated Services):
1. Deploy frontend to Vercel/Netlify as static site
2. Deploy backend to Railway/Render as API
3. Configure CORS on backend
4. Update frontend API base URL

### Phase 3 (Production-Ready):
1. Move to Azure Container Apps or AWS ECS
2. Add Redis cache (replacing in-memory)
3. Add CDN (Azure Front Door / CloudFlare)
4. Implement proper monitoring and logging

## Related Decisions
- [ADR 001: Frontend Framework](001-frontend-framework.md) - React build output served by FastAPI
- [ADR 002: LLM and Agent Framework](002-llm-and-agent-framework.md) - LangGraph agents run in backend
- [ADR 003: Caching Strategy](003-caching-strategy.md) - In-memory cache works well with single instance

## Implementation Checklist
- [ ] Create multi-stage Dockerfile (Node build + Python runtime)
- [ ] Configure FastAPI to serve static files
- [ ] Set up environment variables for API keys
- [ ] Create deployment guide for Railway/Render
- [ ] Add health check endpoint (`/health`)
- [ ] Configure proper logging
- [ ] Document local Docker development workflow

## Notes
This architecture prioritizes **getting started quickly** over architectural purity. It's perfect for:
- Learning full-stack development
- Creating demos and prototypes
- Teaching deployment concepts
- Building portfolio projects

The simplicity here is a feature, not a bug. We can always evolve the architecture as needs grow.
