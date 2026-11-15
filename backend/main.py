import os, re, secrets, hashlib, hmac, base64, time
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from ai_features import router as ai_router

frontend_urls = [url.strip() for url in os.getenv("FRONTEND_URLS", "http://localhost:5173,http://localhost:3000,https://ai-utkarsh-frontend-ex54.vercel.app").split(",") if url.strip()]
mongodb_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME", "ai_utkarsh")
TOKEN_SECRET = os.getenv("TOKEN_SECRET", "")
app = FastAPI(title="AI UTKARSH API", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=frontend_urls, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
mongo_client = AsyncIOMotorClient(mongodb_uri, serverSelectionTimeoutMS=5000) if mongodb_uri else None
db = mongo_client[db_name] if mongo_client else None
app.include_router(ai_router)

class ContactMessage(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=120)
    message: str = Field(..., min_length=10, max_length=2000)

class RegisterInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class ProfileUpdate(BaseModel):
    college: str = Field("", max_length=120)
    degree: str = Field("B.Tech CSE", max_length=80)
    semester: int = Field(1, ge=1, le=12)
    target_role: str = Field("AI/ML Engineer", max_length=100)
    daily_hours: float = Field(2, ge=0, le=16)
    skills: dict[str, int] = Field(default_factory=dict)

def require_db():
    if db is None: raise HTTPException(503, "Database is not configured. Add MONGODB_URI in Render.")

def password_hash(password, salt=None):
    salt=salt or secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,260000)
    return base64.b64encode(salt).decode()+":"+base64.b64encode(digest).decode()

def verify_password(password, stored):
    try:
        salt_b64,digest_b64=stored.split(":")
        candidate=password_hash(password,base64.b64decode(salt_b64)).split(":")[1]
        return hmac.compare_digest(candidate,digest_b64)
    except Exception: return False

def make_token(user_id):
    if not TOKEN_SECRET: raise HTTPException(503,"Authentication is not configured. Add TOKEN_SECRET in Render.")
    payload=f"{user_id}:{int(time.time())+604800}"
    encoded=base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    signature=base64.urlsafe_b64encode(hmac.new(TOKEN_SECRET.encode(),encoded.encode(),hashlib.sha256).digest()).decode().rstrip("=")
    return encoded+"."+signature

async def current_user(authorization: str | None):
    require_db()
    if not authorization or not authorization.startswith("Bearer "): raise HTTPException(401,"Please sign in.")
    try:
        encoded,signature=authorization[7:].split(".")
        expected=base64.urlsafe_b64encode(hmac.new(TOKEN_SECRET.encode(),encoded.encode(),hashlib.sha256).digest()).decode().rstrip("=")
        if not TOKEN_SECRET or not hmac.compare_digest(signature,expected): raise ValueError()
        payload=base64.urlsafe_b64decode(encoded+"="*(-len(encoded)%4)).decode()
        uid,expiry=payload.rsplit(":",1)
        if int(expiry)<int(time.time()): raise ValueError()
    except Exception: raise HTTPException(401,"Session expired. Please sign in again.")
    user=await db.users.find_one({"_id":uid},{"password_hash":0})
    if not user: raise HTTPException(401,"Account not found.")
    return user

@app.get("/")
async def root():
    return {"message":"AI UTKARSH API is running","docs":"/docs","version":"3.0.0"}

@app.get("/api/health")
async def health():
    if db is None:return {"status":"ok","service":"ai-utkarsh-api","database":"not_configured"}
    try:await db.command("ping");database="connected"
    except Exception:database="unavailable"
    return {"status":"ok","service":"ai-utkarsh-api","database":database}

@app.get("/api/projects")
async def projects():
    return {"projects":[
        {"name":"AI UTKARSH","category":"Academic + AI","status":"active"},
        {"name":"House Price Predictor","category":"ML + FastAPI","status":"deployed"},
        {"name":"AI Resume Analyzer","category":"NLP + FastAPI","status":"active"},
        {"name":"SkillBridge AI","category":"GenAI + Full-Stack","status":"deployed"},
        {"name":"AI Traffic Signal Optimizer","category":"Computer Vision","status":"prototype"}]}

@app.post("/api/auth/register")
async def register(data:RegisterInput):
    require_db()
    email=str(data.email).lower().strip()
    if await db.users.find_one({"email":email}):raise HTTPException(409,"An account with this email already exists.")
    uid=secrets.token_urlsafe(16)
    profile={"college":"","degree":"B.Tech CSE","semester":1,"target_role":"AI/ML Engineer","daily_hours":2,"skills":{}}
    doc={"_id":uid,"name":data.name.strip(),"email":email,"password_hash":password_hash(data.password),"profile":profile,"created_at":datetime.now(timezone.utc)}
    try:await db.users.insert_one(doc)
    except Exception:raise HTTPException(503,"Could not create account. Please try again.")
    return {"token":make_token(uid),"user":{"id":uid,"name":doc["name"],"email":email,"profile":profile}}

@app.post("/api/auth/login")
async def login(data:LoginInput):
    require_db()
    user=await db.users.find_one({"email":str(data.email).lower().strip()})
    if not user or not verify_password(data.password,user.get("password_hash","")):raise HTTPException(401,"Incorrect email or password.")
    return {"token":make_token(user["_id"]),"user":{"id":user["_id"],"name":user["name"],"email":user["email"],"profile":user.get("profile",{})}}

@app.get("/api/profile/me")
async def get_profile(authorization:str|None=Header(default=None)):
    user=await current_user(authorization)
    return {"user":{"id":user["_id"],"name":user["name"],"email":user["email"],"profile":user.get("profile",{})}}

@app.put("/api/profile/me")
async def update_profile(data:ProfileUpdate,authorization:str|None=Header(default=None)):
    user=await current_user(authorization)
    profile=data.model_dump()
    profile["skills"]={str(k)[:40]:max(0,min(100,int(v))) for k,v in profile["skills"].items()}
    await db.users.update_one({"_id":user["_id"]},{"$set":{"profile":profile,"updated_at":datetime.now(timezone.utc)}})
    return {"success":True,"profile":profile}

@app.post("/api/contact")
async def contact(message:ContactMessage):
    if db is None:raise HTTPException(503,detail="Database is not configured.")
    document=message.model_dump();document["received_at"]=datetime.now(timezone.utc)
    try:result=await db.contact_messages.insert_one(document)
    except Exception:raise HTTPException(503,detail="Unable to save your message right now.")
    return {"success":True,"message":"Thanks! Your message has been received.","id":str(result.inserted_id)}
