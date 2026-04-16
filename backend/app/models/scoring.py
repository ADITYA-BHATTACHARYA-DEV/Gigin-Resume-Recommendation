from pydantic import BaseModel

class ScoringWeights(BaseModel):
    """Phase 5: Configurable weights for the Global Scoring Formula [cite: 317]"""
    w_semantic: float = 0.5   # Relevance focus
    w_depth: float = 0.2      # Career growth focus
    w_stability: float = 0.2  # Retention focus
    w_risk: float = 0.1       # Forensic risk penalty focus