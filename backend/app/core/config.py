import os

class Settings:
    # Phase 5: Global Weights [cite: 317, 318]
    # Standard balance: Stability 20%, Skill Match 50% [cite: 436]
    W_SEMANTIC: float = 0.5
    W_DEPTH: float = 0.2
    W_STABILITY: float = 0.2
    W_RISK: float = 0.1 
    
    CHROMA_PATH: str = "data/chroma_db"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2" # 384d Vectors [cite: 350]

settings = Settings()