from sqlalchemy import Column, String, Integer, Float, Date
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    dob = Column(Date)
    contact_number = Column(String)
    address = Column(String)
    qualification = Column(String)
    graduation_year = Column(Integer)
    experience = Column(Float)
    skills = Column(String)
    resume_name = Column(String)