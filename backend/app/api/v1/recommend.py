# from fastapi import APIRouter, Query
# from typing import List
# import numpy as np

# from app.services.chroma_service import chroma_service
# from app.services.mmr_logic import apply_mmr_diversification
# from app.services.scoring_engine import ScoringEngine
# from app.services.agents import RecruitmentAgents
# from app.core.database import db, redis_client

# router = APIRouter()
# agents = RecruitmentAgents()
# print("--- AGENT METHODS DETECTED ---")
# print([method for method in dir(agents) if not method.startswith('_')])
# @router.get("/recommend")
# async def get_smart_recommendations(jd_query: str = Query(...), lambda_val: float = 0.5):
#     print(f"--- 🔎 SEARCHING FOR: {jd_query} ---")
#     """
#     Unrestricted RAG Pipeline:
#     Uses Folder Metadata as a 'Ranking Signal' rather than a 'Hard Filter'.
#     """
    
#     # --- PHASE 2: Broad Vector Retrieval (The 'R') ---
#     # We remove the 'where' filter to ensure we ALWAYS get results.
#     # We retrieve the top 50 most semantically relevant profiles globally.
#     raw_results = chroma_service.collection.query(
#         query_texts=[jd_query],
#         n_results=50,
#         include=["documents", "metadatas", "embeddings", "distances"]
#     )

#     # DEBUG: Check if ChromaDB sees anything at all
#     found_count = len(raw_results['ids'][0]) if raw_results['ids'] else 0
#     print(f"--- 📊 CHROMA RESULTS: {found_count} matches found ---")

#     if found_count == 0:
#         # If this prints 0, your ChromaDB is pointing to the wrong folder on F:
#         print("🚨 ERROR: ChromaDB index appears empty or collection name is mismatched.")
#         return []

#     if not raw_results['ids'] or not raw_results['ids'][0]:
#         print("--- DEBUG: ChromaDB HNSW Index is empty or unreachable ---")
#         return []

#     # --- PHASE 3: MMR Diversification ---
#     # Reduces redundancy in the top 50 to get a diverse Top 15.
#     top_15_indices = apply_mmr_diversification(
#         query_emb=raw_results['embeddings'][0][0], 
#         candidate_embs=raw_results['embeddings'][0], 
#         lambda_val=lambda_val,
#         k=min(15, len(raw_results['ids'][0]))
#     )

#     shortlist = []
#     query_lower = jd_query.lower()

#     for idx in top_15_indices:
#         candidate_id = raw_results['ids'][0][idx]
#         metadata = raw_results['metadatas'][0][idx]
#         text = raw_results['documents'][0][idx]
        
#         # --- PHASE 4: Metadata Signal Detection ---
#         # Instead of blocking, we check if the folder matches the query.
#         # This handles nested 'Telesales/Bangalore' or 'IT/Remote/Senior' folders.
#         folder_bonus = 0.0
#         role_tag = metadata.get("role", "").lower()
#         loc_tag = metadata.get("location", "").lower()

#         if role_tag in query_lower: folder_bonus += 0.1
#         if loc_tag in query_lower: folder_bonus += 0.1

#         # --- PHASE 5: The Mathematical Funnel ---
#         # S_total = (w_sem * S_sem) + (w_dep * S_dep) + (w_sta * S_sta) - (w_risk * S_risk)
        
#         s_sem_raw = 1 - raw_results['distances'][0][idx]
#         s_sem_weighted = s_sem_raw + folder_bonus # Folder match adds a 'Context Bonus'
        
#         # Forensic Risk Audit (Phase 4.2)
#         s_risk = agents.auditor_agent(text) 
        
#         final_score = ScoringEngine.get_final_score(
#             s_sem=min(s_sem_weighted, 1.0), # Cap at 1.0
#             s_dep=0.75, 
#             s_sta=0.85, 
#             s_risk=s_risk
#         )

#             # --- PHASE 4: Telemetry ---
#         try:
#             # Only try to log if Redis is actually alive
#             await redis_client.lpush("search_history", jd_query)
#         except Exception:
#             pass # Silently skip if Redis is not installed yet

#         return sorted(shortlist, key=lambda x: x['score'], reverse=True)

#         # --- PHASE 6: Agentic Generation (The 'G') ---
#         # Generate the pitch only for this mathematically verified candidate.
#         try:
#             if hasattr(agents, 'headhunter_pitch'):
#                 pitch = agents.headhunter_pitch(jd_query, text)
#             else:
#                 # Fallback to the method name seen in your debug log
#                 pitch = agents.explainer_agent(jd_query, text)
#         except Exception as e:
#             print(f"Agent Error: {e}")
#             pitch = "Candidate shows strong technical alignment with job requirements."

#         shortlist.append({
#             "candidate_id": candidate_id,
#             "score": round(final_score * 100, 1),
#             "pitch": pitch,
#             "metadata": {
#                 "name": metadata.get("name", "Candidate"),
#                 "role": metadata.get("role", "General"),
#                 "location": metadata.get("location", "N/A"),
#                 "path": metadata.get("path", "")
#             },
#             "score_breakdown": {
#                 "s_sem": round(s_sem_raw * 100, 1),
#                 "folder_boost": round(folder_bonus * 100, 1),
#                 "s_risk": round(s_risk * 100, 1)
#             }
#         })

#     # Record the search in Redis for Phase 4 Telemetry
#     await redis_client.lpush("search_history", jd_query)

#     return sorted(shortlist, key=lambda x: x['score'], reverse=True)



from fastapi import APIRouter, Query
from typing import List
import numpy as np

from app.services.chroma_service import chroma_service
from app.services.mmr_logic import apply_mmr_diversification
from app.services.scoring_engine import ScoringEngine
from app.services.agents import RecruitmentAgents
from app.core.database import redis_client

router = APIRouter()
agents = RecruitmentAgents()

# Debug: Verifying the "Brain" is loaded correctly
print("--- 🧠 AGENT METHODS DETECTED ---")
print([method for method in dir(agents) if not method.startswith('_')])

@router.get("/recommend")
async def get_smart_recommendations(jd_query: str = Query(...), lambda_val: float = 0.5):
    """
    Unrestricted RAG Pipeline:
    1. Retrieval -> 2. MMR -> 3. Scoring (Math Funnel) -> 4. Generation (Pitch)
    """
    print(f"\n--- 🔎 SEARCHING FOR: {jd_query} ---")
    
    # --- PHASE 2: Broad Vector Retrieval (The 'R' in RAG) ---
    raw_results = chroma_service.collection.query(
        query_texts=[jd_query],
        n_results=50,
        include=["documents", "metadatas", "embeddings", "distances"]
    )

    found_count = len(raw_results['ids'][0]) if raw_results['ids'] and raw_results['ids'][0] else 0
    print(f"--- 📊 CHROMA RESULTS: {found_count} matches found ---")

    if found_count == 0:
        return []

    # --- PHASE 3: MMR Diversification ---
    # Ensures the Top 15 are unique talent profiles
    try:
        top_15_indices = apply_mmr_diversification(
            query_emb=raw_results['embeddings'][0][0], 
            candidate_embs=raw_results['embeddings'][0], 
            lambda_val=lambda_val,
            k=min(15, found_count)
        )
    except Exception as e:
        print(f"⚠️ MMR Fallback: {e}")
        top_15_indices = list(range(min(15, found_count)))

    shortlist = []
    query_lower = jd_query.lower()

    # --- LOOP START: Processing the unique candidates ---
    for idx in top_15_indices:
        try:
            candidate_id = raw_results['ids'][0][idx]
            metadata = raw_results['metadatas'][0][idx]
            text = raw_results['documents'][0][idx]
            
            # --- PHASE 4: Metadata Signal Detection (Soft Boost) ---
            folder_bonus = 0.0
            role_tag = metadata.get("role", "").lower()
            loc_tag = metadata.get("location", "").lower()

            if role_tag and role_tag in query_lower: folder_bonus += 0.1
            if loc_tag and loc_tag in query_lower: folder_bonus += 0.1

            # --- PHASE 5: The Mathematical Funnel ---
            # S_total = (w_sem * S_sem) + (w_dep * S_dep) + (w_sta * S_sta) - (w_risk * S_risk)
            s_sem_raw = 1 - raw_results['distances'][0][idx]
            s_sem_weighted = min(s_sem_raw + folder_bonus, 1.0)
            
            s_risk = agents.auditor_agent(text) 
            
            final_score = ScoringEngine.get_final_score(
                s_sem=s_sem_weighted, 
                s_dep=0.75, 
                s_sta=0.85, 
                s_risk=s_risk
            )

            # --- PHASE 6: Agentic Generation (The 'G' in RAG) ---
            try:
                # Check for the specific method name identified in your logs
                if hasattr(agents, 'headhunter_pitch'):
                    pitch = agents.headhunter_pitch(jd_query, text)
                else:
                    pitch = agents.explainer_agent(jd_query, text)
            except Exception as e:
                print(f"⚠️ Pitch Generation Error: {e}")
                pitch = "Candidate shows strong technical alignment based on semantic retrieval."

            # Append to list (Indented inside the loop)
            shortlist.append({
                "candidate_id": candidate_id,
                "score": round(final_score * 100, 1),
                "pitch": pitch,
                "metadata": {
                    "name": metadata.get("name", "Candidate"),
                    "role": metadata.get("role", "General"),
                    "location": metadata.get("location", "N/A"),
                    "path": metadata.get("path", "")
                },
                "score_breakdown": {
                    "s_sem": round(s_sem_raw * 100, 1),
                    "folder_boost": round(folder_bonus * 100, 1),
                    "s_risk": round(s_risk * 100, 1)
                }
            })

        except Exception as e:
            print(f"❌ Skipping candidate {idx} due to error: {e}")
            continue

    # --- PHASE 4: Telemetry (Bypass Redis if offline) ---
    try:
        await redis_client.lpush("search_history", jd_query)
    except Exception:
        pass 

    # --- FINAL RETURN (Outside the loop!) ---
    print(f"✅ Returning {len(shortlist)} candidates to Dashboard.")
    return sorted(shortlist, key=lambda x: x['score'], reverse=True)