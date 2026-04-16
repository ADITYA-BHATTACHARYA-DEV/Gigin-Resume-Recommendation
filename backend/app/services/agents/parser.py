from .base_agent import BaseAgent

class ParserAgent(BaseAgent):
    def extract_structured_data(self, resume_text: str):
        """Phase 4: Extracts structured JSON (Experience, Years, Skills) [cite: 369]"""
        prompt = f"""
        Extract professional DNA from the following resume text into JSON format:
        - Full Name
        - Skills (technical, soft)
        - Experience Years
        - Career Path (list of job titles in chronological order)
        - Company History (list of organization names)
        
        Resume: {resume_text}
        """
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content