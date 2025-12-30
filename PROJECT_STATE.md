# Deliberation AI — Current Project State

## What this project is
A deliberation-first AI system where multiple agents generate competing viewpoints,
a judge agent evaluates reasoning quality, and a synthesizer produces a final answer.

This is a portfolio / demo project focused on AI system design, not model size.

---

## Backend (COMPLETE)
- Framework: FastAPI
- Server: Uvicorn running on http://127.0.0.1:8000
- Endpoints: 
  - `GET /api/` - Health check
  - `POST /api/debate` - Main deliberation endpoint
- CORS enabled for frontend communication
- **Monorepo ready**: Routes use `/api` prefix for unified deployment

Pipeline:
1. Runs deliberation 3 times (for confidence calculation)
2. Each run:
   - Pro agent generates a viewpoint
   - Con agent generates an opposing viewpoint
   - Alternative agent reframes the issue
   - Judge agent scores reasoning and picks a winner
   - Synthesizer produces a final answer
3. Calculates confidence score using **OpenRouter embeddings API**:
   - Generates embeddings for 3 final answers using text-embedding-3-small
   - Computes average pairwise cosine similarity
   - Thresholds:
     - similarity >= 0.9 → High confidence
     - 0.7 <= similarity < 0.9 → Medium confidence  
     - similarity < 0.7 → Low confidence
4. Returns primary (first run) results with confidence

LLM:
- **OpenRouter API** (https://openrouter.ai/api/v1/chat/completions)
- **Model**: deepseek/deepseek-chat
- **Cost**: ~$0.14 per 1M tokens input, ~$0.28 per 1M tokens output
- **Embeddings**: openai/text-embedding-3-small (~$0.00002 per 1K tokens)

Output structure (API response):
- question (string)
- final_answer (string)
- judge_decision (string)
- confidence (string: "high" | "medium" | "low")
- what_would_change (string | null) — only included when confidence is low
- raw_agents { pro, con, alternative }

---

## Frontend (COMPLETE)
- Tech: React + Vite
- Running on: http://localhost:5173/
- No Tailwind, no heavy UI libraries
- Minimal, clean UI
- Single page app
- **Monorepo ready**: Calls `/api/debate` (same domain in production)

Features implemented:
- Textarea for question input
- **3 example questions** for quick testing
- Submit button ("Run Deliberation")
- Loading indicator while waiting for response
- Final answer displayed prominently in highlighted box
- Confidence badge displayed next to final answer (high/medium/low with color coding)
- **"What Would Change This Answer?" section** (appears only when confidence is low)
- Collapsible sections for:
  - Judge decision
  - Pro agent response
  - Con agent response
  - Alternative agent response
- Error handling for failed requests

Technical details:
- Calls POST `/api/debate` (uses `/api` prefix for monorepo deployment)
- Uses environment variable: `VITE_API_URL` (defaults to `/api` in production)
- Handles loading states and errors gracefully
- Displays confidence with color-coded badges:
  - High: green background
  - Medium: yellow background
  - Low: red background
- Conditionally shows "what would change" suggestion when available

---

## Recent Updates

### OpenRouter API Migration (Latest)
- **Replaced local Ollama** with OpenRouter API for chat completions
- **Removed sentence-transformers** (~500MB) and replaced with OpenRouter embeddings API
- **Deployment-ready**: No heavy ML dependencies, suitable for Vercel/Railway/Heroku
- **Cost-efficient**: ~$0.50 per 1K questions (chat: ~$0.49, embeddings: ~$0.006)
- **Environment variables**: OPENROUTER_API_KEY, OPENROUTER_MODEL

### Confidence Scoring System
- Backend runs deliberation 3 times per question
- **Uses OpenRouter embeddings API (text-embedding-3-small) to measure similarity**
- Calculates average pairwise cosine similarity across the 3 answers
- Derives confidence level based on semantic similarity thresholds:
  - **High**: similarity >= 0.9 (answers mean essentially the same thing)
  - **Medium**: 0.7 <= similarity < 0.9 (partial agreement)
  - **Low**: similarity < 0.7 (significant disagreement)
- Added `confidence` field to API response
- Frontend displays confidence badge with color coding

### "What Would Change" Feature
- When confidence is low, backend automatically generates a follow-up prompt
- Asks what additional information would change the answer
- Displayed in frontend only when present
- Helps users understand what's missing or ambiguous

### UI Enhancements
- Constrained max width (760px) for better readability
- Prominent final answer card with larger font and green border
- Muted reasoning sections with smaller, lighter text
- 3 example questions for quick testing
- Collapsible sections for judge decision and raw agent responses

### Status
- ✅ Backend fully functional with OpenRouter API and embeddings
- ✅ Frontend complete with all features
- ✅ Both services running and connected
- ✅ CORS configured for cross-origin requests
- ✅ **Monorepo deployment ready** (single URL, no CORS issues)
- ✅ **Industry best practices** (unified deployment like Next.js)

---

## Non-goals
- No authentication
- No database
- No deployment yet
- No over-styling

---

## Important constraints
- Keep frontend thin; all logic lives in backend
- Do not rewrite backend logic
- API contract is stable and documented above
- All new features should add optional fields, not break existing ones
