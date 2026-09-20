from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers.bugs import router as bugs_router
from app.routers.users import router as users_router
from app.routers.predictions import router as predictions_router

# Import models before creating tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Bug Triage System",
    description="Backend API for the AI-Powered Bug Triage System",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "AI-Powered Bug Triage System Backend is running"
    }


app.include_router(users_router)
app.include_router(bugs_router)
app.include_router(predictions_router)