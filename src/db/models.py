from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    national_id = Column(String, index=True)
    age = Column(Integer)
    sex = Column(String)
    complaints = Column(JSON)
    urgency_score = Column(Integer)
    top_prediction = Column(JSON)
    differentials = Column(JSON)
    evidences = Column(JSON, nullable=True)
    initial_evidence = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
