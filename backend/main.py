import os
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Mehuli Portfolio API",
    description="Backend API for the AI-UTKARSH portfolio.",
    version="1.0.0",
)

frontend_urls = os.getenv(
    "FRONTEND_URLS",
    "http://localhost:5173,http://localhost:3000,https://ai-utkarsh.vercel.app",
)
allowed_origins = [url.strip() for url in frontend_urls.split(",") if url.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactMessage(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=120)
    message: str = Field(..., min_length=10, max_length=2000)


@app.get("/")
def root():
    return {"message": "Mehuli Portfolio API is running", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ai-utkarsh-api"}


@app.get("/api/projects")
def projects():
    return {
        "projects": [
            {"name": "House Price Predictor", "category": "ML + FastAPI", "status": "deployed"},
            {"name": "AI Resume Analyzer", "category": "NLP + FastAPI", "status": "active"},
            {"name": "SkillBridge AI", "category": "GenAI + Full-Stack", "status": "deployed"},
            {"name": "AI Traffic Signal Optimizer", "category": "Computer Vision", "status": "prototype"},
        ]
    }


@app.post("/api/contact")
def contact(message: ContactMessage):
    # This API validates incoming messages and logs them server-side.
    # Add an email provider or database later without changing the frontend contract.
    received_at = datetime.now(timezone.utc).isoformat()
    print(
        f"[CONTACT] {received_at} | {message.name} <{message.email}> | "
        f"{message.subject} | {message.message}"
    )
    return {
        "success": True,
        "message": "Thanks! Your message has been received.",
        "received_at": received_at,
    }
