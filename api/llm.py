import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Try a free model that definitely works
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")

print(f"API Key loaded: {'Yes' if OPENROUTER_API_KEY else 'No'}")
print(f"API Key length: {len(OPENROUTER_API_KEY)}")
print(f"API Key starts with: {OPENROUTER_API_KEY[:10] if OPENROUTER_API_KEY else 'EMPTY'}...")
print(f"Model: {OPENROUTER_MODEL}")

def call_llm(prompt: str) -> str:
    """Call OpenRouter API (supports DeepSeek, GPT-4, Claude, etc.)"""
    if not OPENROUTER_API_KEY:
        error_msg = "OPENROUTER_API_KEY not found in environment variables. Please add it in Vercel dashboard."
        print(f"ERROR: {error_msg}")
        raise ValueError(error_msg)
    
    print(f"Calling OpenRouter with model: {OPENROUTER_MODEL}")
    print(f"Full API key for debugging: {OPENROUTER_API_KEY}")
    
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://deliberation-ai.vercel.app",
                "X-Title": "Deliberation AI"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=120
        )
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text[:500]}")
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip()
        print(f"OpenRouter response received: {len(result)} chars")
        return result
    except Exception as e:
        print(f"ERROR in call_llm: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        raise
