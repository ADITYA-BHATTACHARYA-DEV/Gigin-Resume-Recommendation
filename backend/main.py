from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# --- MISSING IMPORT BELOW ---
from fastapi.middleware.cors import CORSMiddleware 
from app.api.v1.ingest import router as ingest_router
from app.api.v1.recommend import router as recommend_router
from app.api.v1.explain import router as explain_router

# 1. Initialize the App
app = FastAPI(title="Lat.ai Recruitment Engine")

# 2. Configure CORS (Cross-Origin Resource Sharing)
# This prevents the "Network Error" you saw in the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount the Static Files for PDF Previews
# Maps F: drive files to http://localhost:8000/resumes
app.mount("/resumes", StaticFiles(directory="F:/Gigin Resume Recommendation/backend"), name="resumes")

# 4. Include Routers with the /api/v1 prefix
app.include_router(ingest_router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(recommend_router, prefix="/api/v1", tags=["Discovery"])
app.include_router(explain_router, prefix="/api/v1", tags=["Explanation"])

@app.get("/")
async def root():
    return {"status": "Operational", "engine": "Lat.ai v1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)