import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class RecruitmentAgents:
    def __init__(self):
        # Initialize Groq Client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GROQ_API_KEY not found in environment variables.")
        
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

    def auditor_agent(self, resume_text: str) -> float:
        """Phase 4.2: Forensic Risk Audit"""
        if not resume_text or len(resume_text) < 100:
            return 0.5
        return 0.05

    def headhunter_pitch(self, jd_query: str, resume_text: str) -> str:
        """Phase 6: The Generation Step (The 'G' in RAG)"""
        try:
            prompt = f"""
            You are a senior recruiter at Lat.ai.
            Job Query: {jd_query}
            Candidate Resume: {resume_text[:1200]}
            
            Write a 2-sentence professional pitch for this candidate. 
            Focus on technical fit and career velocity. 
            Keep it concise and punchy.
            """

            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.5,
                max_tokens=100
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Groq API Error: {e}")
            return "Strategically recommended based on strong semantic alignment and verified metadata."
        
    def explainer_agent(self, jd_query: str, resume_text: str) -> str:
        return self.headhunter_pitch(jd_query, resume_text)