from app.core.config import settings

class ScoringEngine:
    @staticmethod
    def calculate_stability(total_months: int, unique_companies: int) -> float:
        """Basis: Average time spent at each organization [cite: 334, 336]"""
        # Stability = Total Months / Number of Unique Companies [cite: 336]
        return total_months / max(unique_companies, 1)

    @staticmethod
    def get_final_score(s_sem: float, s_dep: float, s_sta: float, s_risk: float) -> float:
        """
        Phase 5: Weighted Composite Scoring [cite: 373, 433]
        Formula: S_total = (w_sem * S_sem) + (w_dep * S_dep) + (w_sta * S_sta) - (w_risk * S_risk) [cite: 317]
        """
        # Normalization: Every sub-score is scaled 0 to 1 [cite: 319]
        score = (settings.W_SEMANTIC * s_sem) + \
                (settings.W_DEPTH * s_dep) + \
                (settings.W_STABILITY * s_sta) - \
                (settings.W_RISK * s_risk)
        
        # Scores are normalized to a 1-100 ranked shortlist [cite: 434, 459]
        return round(max(score, 0) * 100, 2)