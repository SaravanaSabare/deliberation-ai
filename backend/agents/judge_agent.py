from llm import call_llm

def judge_agent(question: str, pro: str, con: str, alt: str) -> str:
    prompt = f"""
[JUDGE AGENT]

You are an impartial judge AI.

Question:
{question}

Candidate Answers:

PRO ANSWER:
{pro}

CON ANSWER:
{con}

ALTERNATIVE ANSWER:
{alt}

Your task:
1. Score each answer from 0–10 based on logical consistency and reasoning quality
2. Pick ONE winner
3. Explain briefly why it won

Return STRICTLY in this format:

Winner:
Scores:
- Pro:
- Con:
- Alternative:
Reason:
"""
    return call_llm(prompt)
