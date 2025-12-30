import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import call_llm

def con_agent(question: str) -> str:
    prompt = f"""
[CON AGENT]
I strongly OPPOSE the common answer.

Question:
{question}

Point out flaws, risks, and counterexamples.
"""
    return call_llm(prompt)
