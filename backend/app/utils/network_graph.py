import networkx as nx

def calculate_career_velocity_slope(titles: list):
    """
    Phase 4: DepthAgent Logic.
    Calculates S_dep based on promotion density[cite: 327, 330].
    Positive signal: Moving Junior -> Mid -> Senior within 4 years[cite: 331].
    """
    if not titles: return 0.0
    
    # Seniority hierarchy mapping [cite: 331]
    hierarchy = {"Junior": 1, "Mid": 2, "Senior": 3, "Lead": 4, "Manager": 5}
    
    slope = 0
    for i in range(len(titles) - 1):
        prev_lvl = hierarchy.get(titles[i], 1)
        curr_lvl = hierarchy.get(titles[i+1], 2)
        if curr_lvl > prev_lvl:
            slope += 1 # Upward trajectory detected [cite: 331]
            
    # Normalized score between 0 and 1 [cite: 319]
    return min(slope / max(len(titles)-1, 1), 1.0)