from fastapi import APIRouter, Query
from app.services.chroma_service import chroma_service
from app.services.mmr_logic import apply_mmr_diversification
from app.services.scoring_engine import ScoringEngine
from app.services.agents import RecruitmentAgents

router = APIRouter()
# Note: Use the singleton instance created in your services
agents = RecruitmentAgents()

@router.get("/")
async def get_smart_recommendations(jd_query: str = Query(...), lambda_val: float = 0.5):
    """
    Executes the 6-Phase Pipeline with Metadata Filtering:
    1. Metadata Extraction -> 2. Retrieval -> 3. Diversify -> 4. Scrutiny -> 5. Score
    """
    
    # --- PHASE 2.1: Metadata Keyword Extraction ---
    # Logic: Detect keywords in the chat input that match your folder names
    query_lower = jd_query.lower()
    where_filter = {}
    
    # Automatic Role Filtering (Example folders)
    if "telesales" in query_lower:
        where_filter["role"] = "Telesales"
    elif "it" in query_lower:
        where_filter["role"] = "IT"

    # Automatic Location Filtering (Example folders)
    if "bangalore" in query_lower:
        where_filter["location"] = "Bangalore"
    elif "mumbai" in query_lower:
        where_filter["location"] = "Mumbai"

    # --- PHASE 2.2: Candidate Generation (Filtered Top 50) ---
    # We query ChromaDB using the 'where' clause for hard folder-based constraints
    # If no keywords found, it performs a global search
    raw_results = chroma_service.collection.query(
        query_texts=[jd_query],
        n_results=50,
        where=where_filter if where_filter else None,
        include=["documents", "metadatas", "embeddings", "distances"]
    )

    if not raw_results['ids'][0]:
        return []

    # --- PHASE 3: MMR Diversification (Top 15 Unique Options) ---
    # MMR ensures we don't return 15 identical Bangalore Telesales profiles
    top_15_indices = apply_mmr_diversification(
        query_emb=raw_results['embeddings'][0][0], # JD Vector
        candidate_embs=raw_results['embeddings'][0], # Pool Vectors
        lambda_val=lambda_val,
        k=min(15, len(raw_results['ids'][0]))
    )

    shortlist = []
    for idx in top_15_indices:
        metadata = raw_results['metadatas'][0][idx]
        text = raw_results['documents'][0][idx]
        
        # --- PHASE 4: Agentic Scrutiny (Forensic Risk) ---
        # The Auditor Agent checks for 'AI DNA' and date anomalies
        s_risk = agents.auditor_agent(text) 
        
        # --- PHASE 5: Mathematical Funnel (Final Ranking) ---
        # S_total = (w1*S_sem) + (w2*S_dep) + (w3*S_sta) - (w4*S_risk)
        final_score = ScoringEngine.get_final_score(
            s_sem=1 - raw_results['distances'][0][idx], # Convert distance to similarity
            s_dep=0.75, # Placeholder: In production, call agents.depth.analyze_trajectory()
            s_sta=0.85, # Placeholder: In production, calculate from parsed JSON
            s_risk=s_risk
        )

        shortlist.append({
            "candidate_id": raw_results['ids'][0][idx],
            "score": final_score,
            "metadata": {
                "name": metadata.get("filename", "Unknown"),
                "role": metadata.get("role", "Unknown"),
                "location": metadata.get("location", "Unknown"),
                "path": metadata.get("path", "")
            },
            # Provide breakdown for the Next.js progress bars
            "score_breakdown": {
                "s_sem": round((1 - raw_results['distances'][0][idx]) * 100, 1),
                "s_dep": 75,
                "s_sta": 85,
                "s_risk": round(s_risk * 100, 1)
            }
        })

    # Sort the unique shortlist by the final weighted score
    return sorted(shortlist, key=lambda x: x['score'], reverse=True)