import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field


frontend_urls = [url.strip() for url in os.getenv("FRONTEND_URLS", "http://localhost:5173,http://localhost:3000").split(",") if url.strip()]
mongodb_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME", "ai_utkarsh")

app = FastAPI(title="Mehuli Portfolio API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = AsyncIOMotorClient(mongodb_uri) if mongodb_uri else None
db = mongo_client[db_name] if mongo_client else None


class ContactMessage(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=120)
    message: str = Field(..., min_length=10, max_length=2000)


@app.get("/")
async def root():
    return {"message": "Mehuli Portfolio API is running", "docs": "/docs"}


@app.get("/api/health")
async def health():
    if db is None:
        return {"status": "ok", "service": "ai-utkarsh-api", "database": "not_configured"}
    try:
        await db.command("ping")
        database = "connected"
    except Exception:
        database = "unavailable"
    return {"status": "ok", "service": "ai-utkarsh-api", "database": database}


@app.get("/api/projects")
async def projects():
    return {"projects": [
        {"name": "House Price Predictor", "category": "ML + FastAPI", "status": "deployed"},
        {"name": "AI Resume Analyzer", "category": "NLP + FastAPI", "status": "active"},
        {"name": "SkillBridge AI", "category": "GenAI + Full-Stack", "status": "deployed"},
        {"name": "AI Traffic Signal Optimizer", "category": "Computer Vision", "status": "prototype"},
    ]}


@app.post("/api/contact")
async def contact(message: ContactMessage):
    if db is None:
        raise HTTPException(status_code=503, detail="Database is not configured.")

    document = message.model_dump()
    document["received_at"] = datetime.now(timezone.utc)

    try:
        result = await db.contact_messages.insert_one(document)
    except Exception:
        raise HTTPException(status_code=503, detail="Unable to save your message right now.")

    return {
        "success": True,
        "message": "Thanks! Your message has been received.",
        "id": str(result.inserted_id),
    }
