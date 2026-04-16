from fastapi import APIRouter, HTTPException
from app.services.agents import RecruitmentAgents # Import the new orchestrator
from app.db.mongodb import MongoDBClient

router = APIRouter()
agents = RecruitmentAgents()
db = MongoDBClient()

@router.post("/explain")
async def get_headhunter_pitch(candidate_id: str, jd_query: str):
    """
    Phase 6: Explanation & Persistence.
    Generates a 'Headhunter's Pitch' using Groq (Llama-3.3 70B).
    """
    # 1. Fetch analyzed candidate data from MongoDB [cite: 380, 383]
    candidate_data = await db.get_candidate_json(candidate_id)
    if not candidate_data:
        raise HTTPException(status_code=404, detail="Candidate analysis not found")

    # 2. Use ExplainerAgent for 'Why' logic [cite: 381, 382]
    # This generates a pitch explaining technical overlap and growth trajectory.
    pitch = agents.explainer_agent(candidate_data, jd_query)

    # 3. Persist the final natural language verdict 
    await db.save_verdict(candidate_id, {"pitch": pitch})

    return {"candidate_id": candidate_id, "pitch": pitch}