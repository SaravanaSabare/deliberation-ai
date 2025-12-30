from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback
from agents.pro_agent import pro_agent
from agents.con_agent import con_agent
from agents.alt_agent import alt_agent
from agents.judge_agent import judge_agent
from synthesizer import synthesize_answer
from llm import call_llm
from semantic_similarity import calculate_semantic_similarity, get_confidence_from_similarity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DebateRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Deliberation AI running"}

@app.post("/debate")
def debate(request: DebateRequest):
    try:
        question = request.question
        print(f"Starting deliberation for question: {question}")
        
        # Run deliberation 3 times to measure confidence
        runs = []
        for i in range(3):
            print(f"Run {i+1}/3")
            pro = pro_agent(question)
            print(f"Pro agent response: {pro[:100] if pro else 'EMPTY'}")
            con = con_agent(question)
            print(f"Con agent response: {con[:100] if con else 'EMPTY'}")
            alt = alt_agent(question)
            print(f"Alt agent response: {alt[:100] if alt else 'EMPTY'}")
            judge = judge_agent(question, pro, con, alt)
            print(f"Judge agent response: {judge[:100] if judge else 'EMPTY'}")
            final_answer = synthesize_answer(question, judge)
            print(f"Final answer: {final_answer[:100] if final_answer else 'EMPTY'}")
            
            runs.append({
                "pro": pro,
                "con": con,
                "alt": alt,
                "judge": judge,
                "final_answer": final_answer
            })
        
        # Calculate confidence based on semantic similarity
        final_answers = [run["final_answer"] for run in runs]
        
        # Use embeddings to measure semantic similarity
        similarity_score = calculate_semantic_similarity(final_answers)
        confidence = get_confidence_from_similarity(similarity_score)
        
        # Use first run as primary output
        primary = runs[0]
        
        # Generate "what would change" only for low confidence
        what_would_change = None
        if confidence == "low":
            disagreement_summary = f"""
The deliberation system ran 3 times and produced semantically different results (similarity: {similarity_score:.2f}):
- Answer 1: {final_answers[0][:100]}...
- Answer 2: {final_answers[1][:100]}...
- Answer 3: {final_answers[2][:100]}...

Question: {question}
"""
            what_would_change_prompt = f"""{disagreement_summary}

Given this disagreement, what additional information or clarification would most likely change or strengthen the conclusion? Be specific and concise."""
            
            what_would_change = call_llm(what_would_change_prompt)
        
        response = {
            "question": question,
            "final_answer": primary["final_answer"],
            "judge_decision": primary["judge"],
            "confidence": confidence,
            "raw_agents": {
                "pro": primary["pro"],
                "con": primary["con"],
                "alternative": primary["alt"]
            }
        }
        
        if what_would_change:
            response["what_would_change"] = what_would_change
        
        return response
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

# Vercel serverless function handler
handler = app
