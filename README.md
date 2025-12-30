# Deliberation AI

> A multi-agent deliberation system that surfaces uncertainty in AI-generated answers through structured debate and confidence measurement.

**🔗 Live Demo**: [https://deliberation-ai.vercel.app](https://deliberation-ai.vercel.app)

---

## 📋 Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Local Development](#local-development)
- [Project Structure](#project-structure)
- [Performance](#performance)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Deliberation AI addresses a critical challenge in AI systems: **overconfidence**. Traditional LLMs often provide answers with unwavering certainty, even when the question is ambiguous or requires additional context.

This system runs a **structured debate** among specialized AI agents, evaluates their reasoning, and measures confidence through semantic similarity. When uncertainty is detected, it explicitly tells you what information would change the answer.

**Use Cases:**
- Decision support systems requiring transparency
- Educational tools that teach critical thinking
- Research assistants that identify knowledge gaps
- Any application where AI uncertainty matters

---

## 🚨 The Problem

Large language models exhibit several problematic behaviors:

1. **Overconfidence**: Providing definitive answers to ambiguous questions
2. **Hidden Uncertainty**: No indication when more context is needed
3. **Single Perspective**: Only one reasoning path, missing alternative viewpoints
4. **Poor Calibration**: Confidence doesn't correlate with accuracy

**Example:**
- **Question**: "Should I invest in cryptocurrency?"
- **Typical LLM**: "Yes, cryptocurrency offers high returns..." *(overconfident)*
- **Deliberation AI**: "It depends on your risk tolerance..." *(confidence: LOW)* + *"Knowing your age and financial goals would change this answer"*

---

## ⚙️ How It Works

### 1. Multi-Agent Deliberation

Five specialized agents participate in each deliberation:

| Agent | Role | Purpose |
|-------|------|---------|
| **Pro Agent** | Argues FOR a position | Generates supporting evidence |
| **Con Agent** | Argues AGAINST the position | Identifies risks and counterpoints |
| **Alternative Agent** | Reframes the question | Provides different perspectives |
| **Judge Agent** | Evaluates reasoning quality | Selects the best argument based on logic |
| **Synthesizer** | Produces final answer | Creates coherent response from judge's decision |

### 2. Confidence Measurement

The system runs the deliberation **once** (optimized for speed) and evaluates the reasoning quality through the judge's evaluation. Future versions will run multiple iterations and measure semantic similarity between outputs to quantify confidence:

| Confidence | Meaning | System Behavior |
|------------|---------|----------------|
| **High** | Strong consensus across agents | Returns answer with high confidence badge |
| **Medium** | Partial agreement | Returns answer with medium confidence badge |
| **Low** | Significant disagreement | Returns answer + "What Would Change This Answer?" |

*Note: Current production version runs a single deliberation for 1-2 minute response time. Multi-run confidence scoring available by changing `range(1)` to `range(3)` in `api/main.py` line 39.*

### 3. Uncertainty Surfacing

When confidence is low, the system generates a "What Would Change This Answer?" section, explicitly stating what additional information would resolve the uncertainty.

---

## 🏗️ Architecture

### System Flow

```
User Question
     ↓
┌────────────────────┐
│   Pro Agent        │ → "Here's why YES..."
├────────────────────┤
│   Con Agent        │ → "Here's why NO..."
├────────────────────┤
│   Alt Agent        │ → "Actually, consider this reframe..."
└────────────────────┘
     ↓
┌────────────────────┐
│   Judge Agent      │ → Evaluates reasoning quality
└────────────────────┘
     ↓
┌────────────────────┐
│   Synthesizer      │ → Produces final answer
└────────────────────┘
     ↓
Final Answer + Confidence Score
```

### Backend (Python)

- **Framework**: FastAPI wrapped in Vercel serverless function (BaseHTTPRequestHandler)
- **API Endpoint**: `POST /api/debate`
- **LLM Provider**: OpenRouter API
- **Model**: `meta-llama/llama-3.2-3b-instruct:free` (default, configurable)
- **Deployment**: Vercel serverless functions

**Key Components:**
- `api/index.py` - Vercel serverless entry point
- `api/main.py` - FastAPI application logic
- `api/llm.py` - OpenRouter API integration
- `api/agents/` - Individual agent implementations
- `api/synthesizer.py` - Answer synthesis logic

### Frontend (React)

- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.2.4
- **Styling**: CSS with custom design
- **Deployment**: Vercel static hosting

**Features:**
- Real-time deliberation display
- Expandable reasoning details
- Confidence badge with explanations
- Responsive design

---

## ✨ Key Features

### 1. Multi-Perspective Analysis
- Three distinct viewpoints (pro, con, alternative) on every question
- Forces exploration of multiple angles before reaching conclusion

### 2. Reasoning Quality Evaluation
- Judge agent scores arguments based on logical coherence, not popularity
- Transparent decision-making process

### 3. Confidence Measurement
- Semantic similarity analysis across deliberation runs
- Explicit uncertainty quantification

### 4. Actionable Uncertainty
- "What Would Change This Answer?" section when confidence is low
- Guides users on what additional information to provide

### 5. Full Transparency
- Complete reasoning chain available to users
- Expandable sections showing all agent responses
- Judge's decision rationale

---

## 🛠️ Technology Stack

### Backend
- **Language**: Python 3.14+
- **Framework**: FastAPI
- **LLM API**: OpenRouter (https://openrouter.ai)
- **Default Model**: meta-llama/llama-3.2-3b-instruct:free
- **Deployment**: Vercel Serverless Functions
- **Dependencies**: fastapi, uvicorn, requests, python-dotenv, pydantic

### Frontend
- **Language**: JavaScript (React)
- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.2.4
- **Deployment**: Vercel Static Hosting

### Infrastructure
- **Platform**: Vercel
- **Monorepo**: Single deployment with `/api/*` backend routes
- **Auto-Deploy**: GitHub integration (push to `main` → automatic deployment)

---

## 📡 API Reference

### POST /api/debate

Runs a deliberation on the provided question.

**Request:**
```json
{
  "question": "Should I invest in cryptocurrency?"
}
```

**Response:**
```json
{
  "question": "Should I invest in cryptocurrency?",
  "final_answer": "It depends on your risk tolerance, financial goals, and time horizon. Cryptocurrency is highly volatile...",
  "judge_decision": "The Con agent provides the most balanced reasoning by acknowledging both potential and risks...",
  "confidence": "low",
  "what_would_change": "Knowing your age, investment timeline, existing portfolio, and risk tolerance would significantly change this recommendation.",
  "raw_agents": {
    "pro": "Cryptocurrency offers significant upside potential...",
    "con": "Cryptocurrency markets are extremely volatile...",
    "alternative": "Instead of asking 'should I invest,' consider 'how much can I afford to lose...'"
  }
}
```

**Fields:**
- `question` (string): The original question
- `final_answer` (string): The synthesized answer from all agent deliberations
- `judge_decision` (string): The judge's evaluation and reasoning
- `confidence` (string): `"high"`, `"medium"`, or `"low"`
- `what_would_change` (string | null): Guidance on resolving uncertainty (only present when confidence is low)
- `raw_agents` (object): Individual agent responses for transparency

**Status Codes:**
- `200 OK`: Deliberation completed successfully
- `400 Bad Request`: Invalid request format
- `500 Internal Server Error`: Server error during deliberation

---

## 🚀 Deployment

### Live Production Deployment

The project is deployed on Vercel with automatic deployments from GitHub.

**Live URL**: [https://deliberation-ai.vercel.app](https://deliberation-ai.vercel.app)

### Deploying Your Own Instance

1. **Fork the Repository**
   ```bash
   git clone https://github.com/SaravanaSabare/deliberation-ai.git
   cd deliberation-ai
   ```

2. **Get OpenRouter API Key**
   - Sign up at [https://openrouter.ai](https://openrouter.ai)
   - Navigate to API Keys section
   - Create a new API key (format: `sk-or-v1-...`)

3. **Deploy to Vercel**
   ```bash
   npm i -g vercel
   vercel
   ```

4. **Configure Environment Variables**
   
   In Vercel Dashboard → Project → Settings → Environment Variables, add:
   
   | Variable | Value | Required |
   |----------|-------|----------|
   | `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |
   | `OPENROUTER_MODEL` | `meta-llama/llama-3.2-3b-instruct:free` | No (has default) |

5. **Enable Auto-Deploy**
   
   Connect your GitHub repository in Vercel Dashboard:
   - Settings → Git → Connect Repository
   - Push to `main` branch → automatic deployment

### Vercel Configuration

The project uses a monorepo structure with a single `vercel.json`:

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/index"
    }
  ]
}
```

- Frontend builds from `frontend/` directory
- Backend runs as serverless function at `/api/*` routes
- All API requests automatically routed to `api/index.py`

---

## 💻 Local Development

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- OpenRouter API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SaravanaSabare/deliberation-ai.git
   cd deliberation-ai
   ```

2. **Backend Setup**
   ```bash
   cd api
   pip install -r requirements.txt
   ```
   
   Create `.env` file in `api/` directory:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running Locally

**Important**: Local development requires running backend and frontend separately. The current codebase is optimized for Vercel deployment.

For local testing, you'll need to:
1. Modify `api/index.py` to run as a standard FastAPI app
2. Run `uvicorn main:app --reload` in the `api/` directory
3. Update `frontend/src/App.jsx` to point to `http://localhost:8000`
4. Run `npm run dev` in the `frontend/` directory

**Recommended**: Test using the live Vercel deployment or deploy your own instance.

---

## 📁 Project Structure

```
deliberation-ai/
├── api/                          # Backend (Python serverless functions)
│   ├── agents/                   # AI agent implementations
│   │   ├── pro_agent.py          # Generates supporting arguments
│   │   ├── con_agent.py          # Generates opposing arguments
│   │   ├── alt_agent.py          # Reframes the question
│   │   └── judge_agent.py        # Evaluates reasoning quality
│   ├── index.py                  # Vercel serverless entry point
│   ├── main.py                   # FastAPI application logic
│   ├── llm.py                    # OpenRouter API integration
│   ├── synthesizer.py            # Answer synthesis
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # Frontend (React + Vite)
│   ├── src/
│   │   ├── App.jsx               # Main React component
│   │   ├── App.css               # Styling
│   │   └── main.jsx              # Entry point
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
│
├── vercel.json                   # Vercel deployment config
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

### Key Files Explained

- **`api/index.py`**: Vercel serverless function that handles HTTP requests using `BaseHTTPRequestHandler`. Routes all `/api/*` requests to the appropriate handler.

- **`api/main.py`**: Contains the core deliberation logic. Currently runs a single deliberation (line 39: `for i in range(1)`) for optimal performance. Change to `range(3)` for multi-run confidence scoring.

- **`api/llm.py`**: Manages all interactions with OpenRouter API. Includes detailed logging and error handling.

- **`frontend/src/App.jsx`**: React component that handles UI and API communication. Uses `VITE_API_URL` environment variable with fallback to `/api`.

- **`vercel.json`**: Configures Vercel to build the frontend and route `/api/*` requests to the Python serverless function.

---

## ⚡ Performance

### Current Performance Metrics

- **Response Time**: 1-2 minutes per deliberation (single run)
- **Model**: meta-llama/llama-3.2-3b-instruct:free (free tier, no costs)
- **Optimization**: Reduced from 3 deliberation runs to 1 for production speed

### Performance Tuning Options

1. **Use Faster Models**
   ```env
   OPENROUTER_MODEL=openai/gpt-3.5-turbo
   ```
   - Significantly faster response times
   - Requires OpenRouter credits

2. **Enable Multi-Run Confidence**
   
   Edit `api/main.py` line 39:
   ```python
   for i in range(3):  # Change from range(1)
   ```
   - Enables semantic similarity-based confidence scoring
   - Increases response time by 3x
   - Provides more accurate confidence measurements

3. **Reduce Agent Complexity**
   - Simplify agent prompts in `api/agents/` files
   - Shorter responses = faster processing

---

## 🤝 Contributing

Contributions are welcome! Here are some areas for improvement:

### High-Priority Enhancements
- [ ] Multi-run confidence scoring with faster models
- [ ] Embeddings-based semantic similarity calculation
- [ ] Caching layer for repeated questions
- [ ] Streaming responses for real-time feedback

### Feature Ideas
- [ ] User authentication and question history
- [ ] Custom agent personalities
- [ ] Export deliberation results to PDF
- [ ] A/B testing different agent prompts
- [ ] Support for multiple LLM providers

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **OpenRouter**: LLM API aggregation platform
- **Vercel**: Deployment and hosting
- **FastAPI**: Backend framework
- **React**: Frontend framework

---

## 📞 Contact & Links

- **Live Demo**: [https://deliberation-ai.vercel.app](https://deliberation-ai.vercel.app)
- **GitHub Repository**: [https://github.com/SaravanaSabare/deliberation-ai](https://github.com/SaravanaSabare/deliberation-ai)
- **Issues**: [GitHub Issues](https://github.com/SaravanaSabare/deliberation-ai/issues)

---

**Built with ❤️ to make AI more transparent and trustworthy.**
