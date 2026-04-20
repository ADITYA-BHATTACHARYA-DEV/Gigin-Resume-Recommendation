from fastapi import APIRouter, Query
from typing import List
import numpy as np
import app.services.agents as agents_module
print(f"📍 ATTENTION: Loading RecruitmentAgents from: {agents_module.__file__}")
# Core Pipeline Services
from app.services.chroma_service import chroma_service
from app.services.mmr_logic import apply_mmr_diversification
from app.services.scoring_engine import ScoringEngine
from app.services.agents import RecruitmentAgents
from app.core.database import redis_client

router = APIRouter()
agents = RecruitmentAgents()

@router.get("/recommend")
async def get_smart_recommendations(jd_query: str = Query(...), lambda_val: float = 0.5):
    """
    Unified RAG Pipeline:
    Retrieval -> MMR -> Dynamic Scoring -> Agentic Pitch -> Response
    """
    print(f"\n--- 🔎 PIPELINE START: {jd_query} ---")
    
    # --- PHASE 1: Retrieval ---
    raw_results = chroma_service.collection.query(
        query_texts=[jd_query],
        n_results=50,
        include=["documents", "metadatas", "embeddings", "distances"]
    )

    found_count = len(raw_results['ids'][0]) if raw_results['ids'] and raw_results['ids'][0] else 0
    if found_count == 0:
        return []

    # --- PHASE 2: MMR (Talent Diversification) ---
    try:
        top_indices = apply_mmr_diversification(
            query_emb=raw_results['embeddings'][0][0], 
            candidate_embs=raw_results['embeddings'][0], 
            lambda_val=lambda_val,
            k=min(15, found_count)
        )
    except Exception as e:
        print(f"⚠️ MMR Fallback: {e}")
        top_indices = list(range(min(15, found_count)))

    shortlist = []
    query_lower = jd_query.lower()

    # --- PHASE 3: Processing Loop ---
    for idx in top_indices:
        try:
            # 1. Basic Data Extraction
            candidate_id = raw_results['ids'][0][idx]
            metadata = raw_results['metadatas'][0][idx]
            text = raw_results['documents'][0][idx]
            
            # 2. Dynamic Attribute Extraction (No more hardcoding!)
            # These calls talk to your agents.py logic
            val_dep = agents.career_velocity_agent(text) 
            val_sta = agents.stability_agent(text)
            val_risk = agents.auditor_agent(text)
            
            # 3. Weighted Semantic Calculation
            # S_sem + Bonus for folder matching (Regional/Role context)
            s_sem_raw = 1 - raw_results['distances'][0][idx]
            folder_bonus = 0.0
            if metadata.get("role", "").lower() in query_lower: folder_bonus += 0.1
            if metadata.get("location", "").lower() in query_lower: folder_bonus += 0.1
            
            s_sem_weighted = min(s_sem_raw + folder_bonus, 1.0)

            # 4. Phase 5: The Mathematical Funnel
            # Applying: $$S_{total} = (w_{sem} \cdot S_{sem}) + (w_{dep} \cdot S_{dep}) + (w_{sta} \cdot S_{sta}) - (w_{risk} \cdot S_{risk})$$
            final_score = ScoringEngine.get_final_score(
                s_sem=s_sem_weighted, 
                s_dep=val_dep, 
                s_sta=val_sta, 
                s_risk=val_risk
            )

            # 5. Phase 6: Agentic Generation (The 'G' in RAG)
            try:
                if hasattr(agents, 'headhunter_pitch'):
                    pitch = agents.headhunter_pitch(jd_query, text)
                else:
                    pitch = agents.explainer_agent(jd_query, text)
            except Exception:
                pitch = "Strategically recommended based on verified technical alignment."

            # 6. Single Compilation (Fixed the duplicate append issue)
            shortlist.append({
                "candidate_id": candidate_id,
                "score": round(final_score * 100, 1),
                "pitch": pitch,
                "metadata": {
                    "name": metadata.get("name", "Candidate").replace('.pdf', ''),
                        "filename": metadata.get("name", "Candidate"),
                    "role": metadata.get("role", "General Talent"),
                    "location": metadata.get("location", "N/A"),
                },
                "score_breakdown": {
                    "s_sem": round(s_sem_raw * 100, 1),
                    "s_dep": round(val_dep * 100, 1),
                    "s_sta": round(val_sta * 100, 1),
                    "s_risk": round(val_risk * 100, 1),
                    "folder_boost": round(folder_bonus * 100, 1)
                }
            })

        except Exception as e:
            print(f"❌ Error at index {idx}: {e}")
            continue

    # --- Telemetry ---
    try:
        await redis_client.lpush("search_history", jd_query)
    except:
        pass 

    print(f"✅ Pipeline Complete: Returning {len(shortlist)} profiles.")
    return sorted(shortlist, key=lambda x: x['score'], reverse=True)