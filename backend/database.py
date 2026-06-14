from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os

# Create database folder if not exists
os.makedirs("../database", exist_ok=True)

# Create SQLite database
engine = create_engine("sqlite:///../database/bizpath.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Roadmap(Base):
    __tablename__ = "roadmaps"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(100))
    user_profile = Column(Text)
    roadmap_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

# Create tables
Base.metadata.create_all(engine)

def save_roadmap(name: str, profile: dict, roadmap: str):
    session = Session()
    record = Roadmap(
        user_name=name,
        user_profile=json.dumps(profile),
        roadmap_text=roadmap
    )
    session.add(record)
    session.commit()
    session.close()

def get_all_roadmaps(name: str):
    session = Session()
    records = session.query(Roadmap).filter(
        Roadmap.user_name == name
    ).order_by(Roadmap.created_at.desc()).all()
    session.close()
    return [{
        "id": r.id,
        "profile": json.loads(r.user_profile),
        "roadmap": r.roadmap_text,
        "created_at": str(r.created_at)
    } for r in records]