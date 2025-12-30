# Deliberation AI - Deployment Guide

## 🚀 Vercel Deployment

This project is configured for Vercel deployment with a monorepo structure.

### Project Structure
```
deliberation-ai/
├── api/                    # Python backend (serverless functions)
│   ├── agents/            # AI agents
│   ├── index.py           # Entry point
│   ├── main.py            # FastAPI logic
│   ├── llm.py             # OpenRouter API
│   ├── requirements.txt   # Python dependencies
│   └── ...
├── frontend/              # React frontend
│   ├── src/
│   ├── dist/              # Build output
│   └── package.json
└── vercel.json            # Deployment config
```

### Environment Variables Required

Set these in Vercel dashboard (Settings → Environment Variables):

1. **OPENROUTER_API_KEY** (Required)
   - Get from: https://openrouter.ai/keys
   - Format: `sk-or-v1-...` (86 characters)
   - Enable for: Production, Preview, Development

2. **OPENROUTER_MODEL** (Optional)
   - Default: `meta-llama/llama-3.2-3b-instruct:free`
   - Alternative: `deepseek/deepseek-chat` (requires credits)

### Deployment Steps

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy via Vercel CLI:**
   ```bash
   vercel --prod
   ```

3. **Or connect to GitHub:**
   - Go to https://vercel.com
   - Import your GitHub repository
   - Vercel auto-detects configuration from `vercel.json`

### Testing Deployment

- Frontend: https://your-app.vercel.app
- API Health: https://your-app.vercel.app/api
- API Endpoint: https://your-app.vercel.app/api/debate

### Troubleshooting

**"User not found" error:**
- Check API key is 86 characters long
- Verify key is enabled on OpenRouter dashboard
- Ensure key is set for Production environment in Vercel

**Empty responses:**
- Check Vercel function logs
- Verify all environment variables are set
- Check OpenRouter account has credits (if using paid models)

**404 errors:**
- Ensure `vercel.json` has correct rewrites
- Check that `api/` folder exists and has `index.py`

### Local Development

Not recommended - use Vercel for deployment. The app is designed for serverless deployment.

### Notes

- The `backend/` folder is not used in deployment (can be deleted)
- Frontend is built during Vercel deployment
- API functions run as serverless Python functions
- Each deliberation takes ~30-60 seconds
