import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

class ChromaService:
    def __init__(self):
        # Tools: Persistent ChromaDB client [cite: 352]
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL
        )
        # HNSW Index Construction for Phase 1 [cite: 187, 352]
        self.collection = self.client.get_or_create_collection(
            name="resumes", 
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"}
        )

    def index_resume(self, candidate_id: str, text: str, metadata: dict):
        """Phase 1: Ingestion & Vectorization """
        self.collection.add(
            ids=[candidate_id],
            documents=[text],
            metadatas=[metadata]
        )

# ADD THIS LINE AT THE BOTTOM:
chroma_service = ChromaService()