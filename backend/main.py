import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Mehuli Portfolio API", version="2.0.0")

frontend_urls = os.getenv("FRONTEND_URLS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[url.strip() for url in frontend_urls if url.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ai_utkarsh")
mongo_client = AsyncIOMotorClient(MONGODB_URI) if MONGODB_URI else None
db = mongo_client[DB_NAME] if mongo_client else None


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
    database = "not_configured"
    if db is not None:
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
