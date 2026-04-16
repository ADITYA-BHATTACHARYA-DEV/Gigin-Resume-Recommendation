import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def apply_mmr_diversification(query_emb, candidate_embs, lambda_val=0.5, k=15):
    """
    Phase 3: Algorithmic Diversification using Maximal Marginal Relevance[cite: 359, 361].
    Formula: $MMR = \arg \max_{D_i \in R \setminus S} [\lambda \cdot Sim(D_i, Q) - (1-\lambda) \cdot \max_{D_j \in S} Sim(D_i, D_j)]$[cite: 392, 423].
    """
    selected = []
    unselected = list(range(len(candidate_embs)))
    
    # 1. Start with the most relevant candidate [cite: 396]
    relevance_scores = cosine_similarity([query_emb], candidate_embs)[0]
    first_pick = np.argmax(relevance_scores)
    selected.append(first_pick)
    unselected.remove(first_pick)

    # 2. Iteratively select next diverse candidate [cite: 389, 422]
    while len(selected) < k and unselected:
        mmr_scores = []
        for i in unselected:
            relevance = relevance_scores[i]
            # Term 2: Penalty for being too similar to already selected list [cite: 427, 428]
            target_emb = candidate_embs[i].reshape(1, -1)
            selected_embs = [candidate_embs[j] for j in selected]
            novelty_penalty = max(cosine_similarity(target_emb, selected_embs)[0])
            
            score = lambda_val * relevance - (1 - lambda_val) * novelty_penalty
            mmr_scores.append((score, i))
            
        selected.append(max(mmr_scores)[1])
        unselected.remove(selected[-1])
        
    return selected # Returns top 15 unique profiles [cite: 363, 386]