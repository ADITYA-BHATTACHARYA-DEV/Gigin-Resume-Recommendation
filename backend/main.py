from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.ingest import router as ingest_router
from app.api.v1.recommend import router as recommend_router
from app.api.v1.explain import router as explain_router

# 1. Initialize the FastAPI app instance (Crucial: must be before any app. calls)
app = FastAPI(title="Lat.ai Recruitment Engine")

# 2. Mount the Static Files (Phase 1: PDF Access)
# This allows the frontend to preview files via http://localhost:8000/resumes/...
app.mount("/resumes", StaticFiles(directory="F:/Gigin Resume Recommendation/backend"), name="resumes")

# 3. Include API Routers (Phase 2-6)
app.include_router(ingest_router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(recommend_router, prefix="/api/v1", tags=["Discovery"])
app.include_router(explain_router, prefix="/api/v1", tags=["Explanation"])

@app.get("/")
async def root():
    return {"message": "Lat.ai Backend is Operational"}

if __name__ == "__main__":
    import uvicorn
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)