import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 

# Import Routers
from app.api.v1.ingest import router as ingest_router
from app.api.v1.recommend import router as recommend_router
from app.api.v1.explain import router as explain_router

# 1. Initialize the App
app = FastAPI(title="Lat.ai Recruitment Engine")

# 2. Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount the Static Files for PDF Previews
# RECTIFIED: We point to the 'backend' folder because your logs show 
# the path starts with 'Telesales/...'. This folder contains 'Telesales'.
BASE_DIR = r"F:\Gigin Resume Recommendation\backend"

if os.path.exists(BASE_DIR):
    app.mount("/resumes", StaticFiles(directory=BASE_DIR), name="resumes")
    print(f"✅ [SYSTEM] Serving PDFs from: {BASE_DIR}")
else:
    print(f"🚨 [ERROR] Resume directory NOT FOUND: {BASE_DIR}")

# 4. Include Routers
app.include_router(ingest_router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(recommend_router, prefix="/api/v1", tags=["Discovery"])
app.include_router(explain_router, prefix="/api/v1", tags=["Explanation"])

@app.get("/")
async def root():
    return {"status": "Operational", "engine": "Lat.ai v1.0"}

if __name__ == "__main__":
    import uvicorn
    # Using 0.0.0.0 makes it accessible on your local network
    uvicorn.run(app, host="0.0.0.0", port=8000)