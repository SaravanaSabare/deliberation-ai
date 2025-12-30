# Deliberation AI

A deliberation-first AI system that addresses LLM overconfidence by generating multiple competing perspectives, evaluating reasoning quality, and measuring uncertainty through repeated deliberations.

**🚀 Deploy to Vercel:** `vercel --prod` ([Full Guide](MONOREPO_DEPLOYMENT.md))

---

## The Problem

Large language models often respond with high confidence even when answers are ambiguous or uncertain. This creates a false sense of reliability and makes it difficult to identify when additional information is needed.

---

## Core Idea

Instead of asking one model for one answer, **Deliberation AI runs a structured debate** among specialized agents:

1. **Pro Agent** — Argues one perspective
2. **Con Agent** — Argues the opposing view
3. **Alternative Agent** — Reframes the question entirely
4. **Judge Agent** — Evaluates reasoning quality and selects the best argument
5. **Synthesizer** — Produces the final answer based on the judge's decision

To measure confidence, the system **runs this entire deliberation 3 times** and compares outcomes:
- **High confidence**: All runs agree
- **Medium confidence**: Partial agreement
- **Low confidence**: Disagreement across runs

When confidence is low, the system automatically generates **"What Would Change This Answer?"** — suggesting what additional information would resolve the uncertainty.

---

## Architecture

### Backend (FastAPI + OpenRouter)
- `/api/debate` endpoint accepts a question
- Runs deliberation pipeline 3 times
- Calculates confidence using semantic similarity (cosine distance) on embeddings
- Returns:
  - `final_answer`
  - `judge_decision`
  - `confidence` (high/medium/low)
  - `what_would_change` (only when confidence is low)
  - `raw_agents` (pro, con, alternative responses)

**LLM**: DeepSeek via OpenRouter API (`deepseek/deepseek-chat`)  
**Embeddings**: OpenAI text-embedding-3-small via OpenRouter API  
**Cost**: ~$0.50 per 1K questions (chat: ~$0.49, embeddings: ~$0.006)

### Frontend (React + Vite)
- Single-page app with minimal styling
- Input question → Run deliberation
- Calls `/api/debate` (same domain, no CORS!)
- Displays:
  - Final answer (prominently)
  - Confidence badge with explanation
  - "What Would Change" section (on low confidence)
  - Collapsible reasoning details (judge + agent responses)

---

## Example Output

**Question**: *Should I invest in cryptocurrency?*

**Final Answer**: *It depends on your risk tolerance, financial goals, and time horizon. Cryptocurrency is highly volatile and speculative.*

**Confidence**: Low

**What Would Change This Answer?**  
*Knowing your age, investment timeline, existing portfolio diversification, and whether you can afford to lose the investment would significantly change the recommendation.*

---

## Confidence Scoring

Confidence is calculated by running the deliberation **3 times** and measuring **semantic similarity** between final answers using embeddings:

| Similarity Score | Confidence Level | What It Means |
|------------------|------------------|---------------|
| ≥ 0.9 | **High** | Final answers are nearly identical in meaning |
| 0.7 - 0.9 | **Medium** | Final answers share core concepts but differ in details |
| < 0.7 | **Low** | Final answers diverge significantly |

This approach surfaces uncertainty **before** the user acts on the answer, even when phrasing differs.

---

## Setup & Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenRouter API key (https://openrouter.ai)

### Backend
```bash
cd backend
pip install fastapi uvicorn requests python-dotenv numpy

# Create .env file with your API key
echo "OPENROUTER_API_KEY=sk-or-v1-your-key-here" > .env
echo "OPENROUTER_MODEL=deepseek/deepseek-chat" >> .env

uvicorn main:app --reload
```
Server runs on http://127.0.0.1:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs on http://localhost:5173 (or 5174 if port is taken)

---

## Deployment

### Vercel Monorepo (Recommended)
This project uses a **monorepo setup** - both frontend and backend deploy to a **single URL**:
- **One deployment**: `vercel --prod` from project root
- **One URL**: Frontend at `/`, API at `/api/debate`
- **No CORS**: Same domain for everything
- **No heavy dependencies**: Uses API-based embeddings instead of local models
- **Cold start**: ~1-2 seconds (API calls only, no model loading)

```bash
# Navigate to project root
cd c:\Users\drjsk\OneDrive\Desktop\deliberation-ai

# Deploy everything at once!
vercel --prod
```

**Environment Variables**: Add `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` in Vercel dashboard

**Full guide**: [MONOREPO_DEPLOYMENT.md](MONOREPO_DEPLOYMENT.md)

### Other Platforms
- **Railway**: Monorepo support with unified deployment
- **Render**: Similar monorepo setup
- **Local**: Run both servers separately (see Setup & Run above)

---

## Project Design Principles

- **No authentication** — demo project
- **No database** — stateless deliberation
- **Minimal styling** — focus on functionality, not design
- **API-based ML** — avoids heavy local models (sentence-transformers ~500MB)
- **Keep frontend thin** — all logic lives in backend

---

## Completed Features

- ✅ Multi-agent deliberation (Pro, Con, Alternative, Judge, Synthesizer)
- ✅ 3-run confidence measurement with semantic similarity
- ✅ "What Would Change" suggestions for low confidence
- ✅ Example questions in UI for quick demos
- ✅ OpenRouter API integration (DeepSeek + embeddings)
- ✅ Deployment-ready (no heavy ML dependencies)

---

## Why This Matters

Most AI systems hide uncertainty. Deliberation AI **makes uncertainty visible and actionable** by:
- Showing when models disagree
- Explaining what information is missing
- Encouraging critical thinking over blind trust

This is a **portfolio demo** showcasing AI system design, not model performance.
