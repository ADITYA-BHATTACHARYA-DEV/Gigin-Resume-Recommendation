from fastapi import FastAPI
from app.api.v1.ingest import router as ingest_router
from app.api.v1.recommend import router as recommend_router
from app.api.v1.explain import router as explain_router
from fastapi.staticfiles import StaticFiles

# Mount the resume directory as a web-accessible route
# Allows the frontend to access: http://localhost:8000/resumes/Telesales/Bangalore/name.pdf
app.mount("/resumes", StaticFiles(directory="F:/Gigin Resume Recommendation/backend"), name="resumes")

app = FastAPI(title="Lat.ai Recruitment Engine")

# Phase 1-6 Endpoints [cite: 385, 386]
app.include_router(ingest_router, tags=["Phase 1: Ingestion"])
app.include_router(recommend_router, tags=["Phase 2-5: Ranking"])
app.include_router(explain_router, tags=["Phase 6: Verdict"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)