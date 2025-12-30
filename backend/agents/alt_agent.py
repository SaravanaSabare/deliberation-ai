from llm import call_llm

def alt_agent(question: str) -> str:
    prompt = f"""
[ALTERNATIVE AGENT]
I provide a different or edge-case perspective.

Question:
{question}

Challenge assumptions others might ignore.
"""
    return call_llm(prompt)
