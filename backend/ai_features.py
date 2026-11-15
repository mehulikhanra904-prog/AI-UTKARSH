import os, json, re
from datetime import date, timedelta
from typing import Literal
import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
import fitz

router = APIRouter(prefix="/api/ai", tags=["AI Learning"])
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

async def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="AI is not configured. Add GEMINI_API_KEY to backend environment variables.")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json={"contents":[{"parts":[{"text":prompt}]}]})
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="AI provider request failed. Check the API key/model configuration.")
    data = response.json()
    try: return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError): raise HTTPException(status_code=502, detail="AI provider returned an empty response.")

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)
    context: str = Field(default="General study", max_length=300)
class QuizRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=200)
    difficulty: Literal["easy","medium","hard"] = "medium"
    count: int = Field(default=5, ge=1, le=15)
class FlashcardRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=200)
    count: int = Field(default=8, ge=2, le=20)
class PlannerRequest(BaseModel):
    subjects: list[str] = Field(min_length=1, max_length=12)
    hours_per_day: float = Field(default=2, ge=0.5, le=12)
    days: int = Field(default=7, ge=1, le=30)
    goal: str = Field(default="Revise concepts and practice questions", max_length=500)

@router.post("/chat")
async def chat(body: ChatRequest):
    answer = await ask_gemini("You are UTKARSH, a friendly expert tutor. Explain clearly, step-by-step, and encourage learning.\nContext: "+body.context+"\nStudent question: "+body.question)
    return {"answer": answer}

@router.post("/quiz")
async def quiz(body: QuizRequest):
    prompt = f"""Create {body.count} {body.difficulty} multiple-choice questions on {body.topic}.
Return ONLY valid JSON array. Each item: {{ "question": "...", "options": ["A...","B...","C...","D..."], "answer": 0, "explanation": "..." }}.
answer is zero-based option index. Ensure correct factual answers."""
    raw = await ask_gemini(prompt)
    match = re.search(r"\[.*\]", raw, re.S)
    try: questions = json.loads(match.group(0) if match else raw)
    except Exception: raise HTTPException(status_code=502, detail="Could not parse quiz response. Please retry.")
    if not isinstance(questions,list): raise HTTPException(status_code=502, detail="Quiz format was invalid.")
    return {"topic":body.topic,"difficulty":body.difficulty,"questions":questions}

@router.post("/flashcards")
async def flashcards(body: FlashcardRequest):
    raw = await ask_gemini(f'Create {body.count} concise study flashcards for "{body.topic}". Return ONLY JSON array of objects with "front" and "back".')
    match = re.search(r"\[.*\]", raw, re.S)
    try: cards=json.loads(match.group(0) if match else raw)
    except Exception: raise HTTPException(status_code=502,detail="Could not parse flashcards. Please retry.")
    return {"topic":body.topic,"flashcards":cards}

@router.post("/study-plan")
async def study_plan(body: PlannerRequest):
    slots=[]
    start=date.today()
    for day in range(body.days):
        subject=body.subjects[day % len(body.subjects)]
        slots.append({"date":str(start+timedelta(days=day)),"day":day+1,"subject":subject,"duration_hours":body.hours_per_day,"task":body.goal})
    return {"plan":slots,"total_hours":round(body.days*body.hours_per_day,2),"note":"Generated study schedule. Adjust it to your class and exam timetable."}

@router.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400,detail="Upload a PDF file.")
    content=await file.read()
    if len(content)>12*1024*1024: raise HTTPException(status_code=413,detail="PDF must be smaller than 12 MB.")
    try:
        doc=fitz.open(stream=content,filetype="pdf")
        text="\n".join(page.get_text() for page in doc)
        doc.close()
    except Exception: raise HTTPException(status_code=400,detail="Unable to read this PDF.")
    if not text.strip(): raise HTTPException(status_code=400,detail="No selectable text found. Scanned PDFs need OCR.")
    summary=await ask_gemini("Summarize these study notes with headings, key concepts, definitions and exam revision points.\n\n"+text[:45000])
    return {"filename":file.filename,"pages":len(content) and "PDF","summary":summary}
