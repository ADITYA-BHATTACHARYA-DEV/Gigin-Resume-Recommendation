import os
import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader

# Project-specific imports
from app.services.ingest import IngestionService
from app.services.chroma_service import chroma_service
from app.core.database import db # MongoDB instance

router = APIRouter()
ingest_service = IngestionService()

@router.post("/ingest")
async def upload_resume(file: UploadFile = File(...)):
    """
    Phase 1: Single File Ingestion & Vectorization
    Used for ad-hoc candidate uploads.
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    temp_path = f"data/{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the single PDF
        result = await ingest_service.process_pdf(temp_path, file.filename)
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/bulk-scan")
async def bulk_scan():
    """
    Phase 1: The Library Crawler
    Crawls the F: drive, extracts metadata (Role/Location), 
    and indexes into both ChromaDB and MongoDB.
    """
    try:
        root_path = Path("F:/Gigin Resume Recommendation/backend")
        count = 0
        
        # Recursively find all PDFs (excluding venv and .next)
        for file_path in root_path.rglob("*.pdf"):
            if any(part in str(file_path) for part in ["venv", ".next", "node_modules"]):
                continue
            
            # Logic for folder-based metadata
            parts = file_path.parts
            role = parts[-3] if len(parts) >= 3 else "General"
            location = parts[-2] if len(parts) >= 2 else "Unknown"
            
            try:
                # 1. Load PDF Content
                loader = PyPDFLoader(str(file_path))
                pages = loader.load()
                text = " ".join([p.page_content for p in pages])
                
                # 2. Vectorize for ChromaDB (Phase 2 Discovery)
                chroma_service.index_resume(
                    candidate_id=str(file_path),
                    text=text,
                    metadata={
                        "role": role, 
                        "location": location, 
                        "name": file_path.name,
                        "path": str(file_path)
                    }
                )
                
                # 3. Persist in MongoDB (Phase 5 Shortlisting)
                await db.candidates.update_one(
                    {"path": str(file_path)},
                    {"$set": {
                        "name": file_path.name, 
                        "role": role, 
                        "location": location, 
                        "raw_text": text[:1000] # Store snippet for preview
                    }},
                    upsert=True
                )
                
                count += 1
                print(f"✅ Indexed: {file_path.name} ({role} | {location})")
                
            except Exception as e:
                print(f"❌ Error indexing {file_path.name}: {e}")
                
        return {
            "status": "success", 
            "indexed_count": count,
            "message": "Bulk scan of F: drive complete."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))