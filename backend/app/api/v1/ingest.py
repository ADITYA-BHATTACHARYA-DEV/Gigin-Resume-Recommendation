from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.ingest import IngestionService

# Create the router instance
router = APIRouter()
ingest_service = IngestionService()

@router.post("/ingest")
async def upload_resume(file: UploadFile = File(...)):
    """
    Phase 1: Ingestion & Vectorization (The Library) 
    Utilizes PyPDFLoader + Recursive Character TextSplitter[cite: 348].
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save file temporarily on F: drive
    temp_path = f"data/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Trigger Semantic Chunking & Vectorization using all-MiniLM-L6-v2 [cite: 349, 350]
    result = await ingest_service.process_pdf(temp_path, file.filename)
    
    # Cleanup temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    return result