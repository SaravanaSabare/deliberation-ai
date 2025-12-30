import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import call_llm

def pro_agent(question: str) -> str:
    prompt = f"""
[PRO AGENT]
I strongly SUPPORT the best possible answer.

Question:
{question}

Answer with confidence and logical reasoning.
"""
    return call_llm(prompt)
