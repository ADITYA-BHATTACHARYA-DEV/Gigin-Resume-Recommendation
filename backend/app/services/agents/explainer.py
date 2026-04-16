from .base_agent import BaseAgent

class ExplainerAgent(BaseAgent):
    def generate_pitch(self, candidate_data: dict, jd_query: str):
        """
        Phase 6: LLM-as-a-Judge natural language verdict[cite: 381, 382].
        Writes a 'Headhunter's Pitch' explaining 'Why'[cite: 382].
        """
        prompt = f"""
        Write a professional Headhunter's Pitch for this candidate:
        Candidate Data: {candidate_data}
        Target Role: {jd_query}
        
        Explain choice based on high technical overlap and growth trajectory[cite: 382].
        """
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )
        return response.choices[0].message.content