from pydantic import BaseModel
from typing import List, Optional

class CandidateProfile(BaseModel):
    """Phase 4 Parser Output [cite: 369]"""
    candidate_id: str
    name: str
    skills: List[str]
    experience_years: float
    current_title: str
    company_history: List[str] # For Velocity Slope [cite: 293]
    unique_companies_count: int # For Stability calculation [cite: 338]
    total_months: int # For Stability calculation [cite: 337]