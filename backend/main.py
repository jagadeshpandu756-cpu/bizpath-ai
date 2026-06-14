from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ai_engine import generate_roadmap
from data_fetcher import get_live_market_data
from database import save_roadmap, get_all_roadmaps

app = FastAPI(title="BizPath AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfile(BaseModel):
    name: str
    location: str
    budget: float
    currency: str
    interests: list
    risk_level: int
    time_horizon: int
    experience: int
    goal: str

@app.get("/style.css")
def css():
    return FileResponse("../frontend/style.css")

@app.get("/app.js")
def js():
    return FileResponse("../frontend/app.js")

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.post("/generate-roadmap")
async def generate(profile: UserProfile):
    market_data = await get_live_market_data(
        profile.location,
        profile.interests
    )
    roadmap = await generate_roadmap(profile, market_data)
    save_roadmap(profile.name, profile.dict(), roadmap)
    return {"roadmap": roadmap, "status": "success"}

@app.get("/roadmaps/{name}")
def get_roadmaps(name: str):
    return get_all_roadmaps(name)