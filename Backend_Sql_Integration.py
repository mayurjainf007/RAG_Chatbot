from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Database Configuration
DATABASE_URL = "postgresql://user:password@localhost/healthcare_policies"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Policy Model
class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

# Create Tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI()

# Fetch Policies
@app.get("/policies/")
def get_policies():
    db = SessionLocal()
    policies = db.query(Policy).all()
    db.close()
    return policies

# Add New Policy
@app.post("/policies/")
def add_policy(title: str, content: str):
    db = SessionLocal()
    new_policy = Policy(title=title, content=content)
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    db.close()
    return new_policy

# Update Existing Policy
@app.put("/policies/{policy_id}")
def update_policy(policy_id: int, title: str = None, content: str = None):
    db = SessionLocal()
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        db.close()
        raise HTTPException(status_code=404, detail="Policy not found")
    if title:
        policy.title = title
    if content:
        policy.content = content
    policy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(policy)
    db.close()
    return policy
