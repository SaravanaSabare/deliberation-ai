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
