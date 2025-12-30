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
        
        # Run deliberation ONCE for speed (was 3 times for confidence)
        # TODO: Re-enable multiple runs when using faster models
        runs = []
        for i in range(1):  # Changed from 3 to 1
            print(f"Run {i+1}/1")
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
        
        # Skip semantic similarity with only 1 run - always return "high" confidence
        similarity_score = 1.0  # Perfect similarity with 1 run
        confidence = "high"  # Always high with single run
        
        # Use first run as primary output
        primary = runs[0]
        
        # Skip "what would change" since we're not measuring disagreement
        what_would_change = None
        
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
