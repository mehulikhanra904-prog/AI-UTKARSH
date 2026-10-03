import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


frontend_urls = [url.strip() for url in required_env("FRONTEND_URLS").split(",") if url.strip()]
mongodb_uri = required_env("MONGODB_URI")
db_name = required_env("DB_NAME")

app = FastAPI(title="Mehuli Portfolio API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = AsyncIOMotorClient(mongodb_uri)
db = mongo_client[db_name]


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
