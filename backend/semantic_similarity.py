import requests
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"
EMBEDDING_MODEL = "openai/text-embedding-3-small"

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Get embeddings from OpenRouter API.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors
    """
    response = requests.post(
        OPENROUTER_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "Deliberation AI"
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": texts
        },
        timeout=30
    )
    response.raise_for_status()
    
    # Extract embeddings from response
    embeddings = [item["embedding"] for item in response.json()["data"]]
    return embeddings

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a_np = np.array(a)
    b_np = np.array(b)
    
    dot_product = np.dot(a_np, b_np)
    norm_a = np.linalg.norm(a_np)
    norm_b = np.linalg.norm(b_np)
    
    return float(dot_product / (norm_a * norm_b))

def calculate_semantic_similarity(texts: list[str]) -> float:
    """
    Calculate average pairwise cosine similarity between texts using API embeddings.
    
    Args:
        texts: List of text strings to compare
        
    Returns:
        Average similarity score between 0 and 1
    """
    if len(texts) < 2:
        return 1.0  # Single text is perfectly similar to itself
    
    # Get embeddings from API
    embeddings = get_embeddings(texts)
    
    # Calculate pairwise cosine similarities
    n = len(texts)
    similarities = []
    for i in range(n):
        for j in range(i + 1, n):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            similarities.append(similarity)
    
    # Return average similarity
    return float(np.mean(similarities))

def get_confidence_from_similarity(similarity: float) -> str:
    """
    Convert semantic similarity score to confidence level.
    
    Args:
        similarity: Average similarity score between 0 and 1
        
    Returns:
        "high", "medium", or "low"
    """
    if similarity >= 0.9:
        return "high"
    elif similarity >= 0.7:
        return "medium"
    else:
        return "low"
