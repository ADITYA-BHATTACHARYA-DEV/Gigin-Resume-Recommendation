from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.chroma_service import chroma_service
import os
from pathlib import Path
from app.services.chroma_service import chroma_service


class IngestionService:
    def __init__(self):
        # Technique: Semantic Chunking [cite: 349]
        # Instead of cutting text at random intervals, we chunk by section.
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_pdf(self, file_path: str, candidate_id: str):
        """
        Phase 1: Ingestion & Vectorization (The Library) [cite: 346]
        Converts text into 384-dimensional vectors stored in Milvus/Chroma[cite: 350, 352].
        """
        # Step 1: Document Extraction using PyPDFLoader 
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # Step 2: Semantic Chunking [cite: 349]
        full_text = " ".join([p.page_content for p in pages])
        chunks = self.splitter.split_text(full_text)
        
        # Step 3: Vectorization & Storage [cite: 350, 352]
        # We index the full text or primary chunks using all-MiniLM-L6-v2
        chroma_service.index_resume(
            candidate_id=candidate_id,
            text=full_text,
            metadata={"source": file_path, "type": "resume"}
        )
        
        return {
            "candidate_id": candidate_id, 
            "status": "Vectorization Complete",
            "chunks_processed": len(chunks)
        }
    async def ingest_nested_directory(self, root_path: str):
        """
        Crawls: F:/.../backend/{Role}/{Location}/{Files}
        Example: Telesales -> Bangalore -> resume.pdf
        """
        ingested = []
        root = Path(root_path)

        for file_path in root.rglob("*.pdf"):
            # Extract metadata from the path structure
            # parts[-3] = Role, parts[-2] = Location
            parts = file_path.parts
            role = parts[-3] if len(parts) >= 3 else "Unknown"
            location = parts[-2] if len(parts) >= 2 else "Unknown"

            try:
                loader = PyPDFLoader(str(file_path))
                pages = loader.load()
                text = " ".join([p.page_content for p in pages])

                # Phase 1: Storage with Nested Metadata
                chroma_service.index_resume(
                    candidate_id=file_path.name,
                    text=text,
                    metadata={
                        "path": str(file_path),
                        "role": role,
                        "location": location,
                        "filename": file_path.name
                    }
                )
                ingested.append(file_path.name)
            except Exception as e:
                print(f"Failed {file_path.name}: {e}")

        return {"status": "success", "count": len(ingested)}