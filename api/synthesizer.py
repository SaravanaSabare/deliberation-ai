from llm import call_llm

def synthesize_answer(question: str, judge_decision: str) -> str:
    prompt = f"""
You are a senior AI system.

Question:
{question}

Judge Decision:
{judge_decision}

Task:
- Produce a single, clear, balanced final answer
- Respect the judge’s chosen reasoning
- Avoid extreme confidence
- Be concise and responsible

Return ONLY the final answer.
"""
    return call_llm(prompt)
