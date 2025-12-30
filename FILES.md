# 📁 Project Files

## Core Files
- **README.md** - Project overview, architecture, local setup
- **PROJECT_STATE.md** - Technical documentation and current state
- **MONOREPO_DEPLOYMENT.md** - Complete deployment guide for Vercel
- **IMPROVEMENT_IDEAS.md** - Future enhancements and optimization ideas
- **vercel.json** - Monorepo deployment configuration

## Structure
```
deliberation-ai/
├── README.md                      ← Start here
├── MONOREPO_DEPLOYMENT.md         ← Deploy guide
├── PROJECT_STATE.md               ← Technical docs
├── IMPROVEMENT_IDEAS.md           ← Future work
├── vercel.json                    ← Deployment config
├── .gitignore                     ← Git exclusions
│
├── backend/
│   ├── main.py                    ← FastAPI app (routes at /api/*)
│   ├── llm.py                     ← OpenRouter integration
│   ├── semantic_similarity.py     ← Embeddings & confidence
│   ├── synthesizer.py             ← Final answer synthesis
│   ├── requirements.txt           ← Python dependencies
│   ├── .env                       ← API keys (not committed)
│   ├── .env.example               ← Environment template
│   └── agents/
│       ├── pro_agent.py
│       ├── con_agent.py
│       ├── alt_agent.py
│       └── judge_agent.py
│
└── frontend/
    ├── src/
    │   ├── App.jsx                ← Main React component
    │   ├── App.css                ← Styles
    │   └── main.jsx               ← Entry point
    ├── package.json               ← Node dependencies
    ├── vite.config.js             ← Vite configuration
    ├── .env.example               ← Environment template
    └── .gitignore                 ← Git exclusions
```

## Quick Reference

### Deploy to Production
```bash
vercel --prod
```

### Run Locally
```bash
# Backend (Terminal 1)
cd backend
uvicorn main:app --reload

# Frontend (Terminal 2)
cd frontend
echo "VITE_API_URL=http://127.0.0.1:8000/api" > .env
npm run dev
```

### Documentation
- **Getting Started**: README.md
- **Deployment**: MONOREPO_DEPLOYMENT.md
- **Architecture**: PROJECT_STATE.md
- **Future Ideas**: IMPROVEMENT_IDEAS.md
