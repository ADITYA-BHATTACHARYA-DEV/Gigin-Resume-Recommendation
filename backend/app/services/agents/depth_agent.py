import networkx as nx
from .base_agent import BaseAgent

class DepthAgent(BaseAgent):
    def analyze_trajectory(self, job_titles: list):
        """
        Uses NetworkX to analyze the 'Career Graph'[cite: 370].
        Calculates the slope: are they getting promoted or jumping laterally? [cite: 371]
        """
        # S_DEP Basis: The 'slope' of a candidate's career [cite: 328]
        # Positive signal: Junior -> Mid -> Senior in < 4 years [cite: 331]
        hierarchy = {"Junior": 1, "Associate": 2, "Senior": 3, "Lead": 4, "Manager": 5}
        
        G = nx.DiGraph()
        slope = 0
        for i in range(len(job_titles) - 1):
            prev_val = hierarchy.get(job_titles[i], 1)
            curr_val = hierarchy.get(job_titles[i+1], 2)
            if curr_val > prev_val:
                slope += 1
                
        # Normalize score based on promotion density [cite: 330]
        return min(slope / max(len(job_titles)-1, 1), 1.0)