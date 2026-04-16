from groq import Groq
from app.core.config import settings

class BaseAgent:
    def __init__(self):
        # Tools: Groq (Llama-3.3 70B) + Regex Guardrails [cite: 368]
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"