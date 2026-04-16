from .parser import ParserAgent
from .depth_agent import DepthAgent
from .auditor import AuditorAgent
from .explainer import ExplainerAgent

class RecruitmentAgents:
    """
    Orchestrator class for Phase 4 (Scrutiny) and Phase 6 (Explanation)[cite: 367, 373].
    This wrapper maintains compatibility with the recommendation pipeline[cite: 386].
    """
    def __init__(self):
        # Tools: Groq (Llama-3.3 70B) + Regex Guardrails [cite: 368]
        self.parser = ParserAgent()
        self.depth = DepthAgent()
        self.auditor = AuditorAgent()
        self.explainer = ExplainerAgent()

    def auditor_agent(self, resume_text: str):
        """Phase 4: Checks for 'AI Patterns' and forensic inconsistencies[cite: 372]."""
        return self.auditor.perform_forensic_audit(resume_text)

    def explainer_agent(self, candidate_data: dict, jd_query: str):
        """Phase 6: Generates the 'Headhunter Pitch' natural language verdict[cite: 382]."""
        return self.explainer.generate_pitch(candidate_data, jd_query)