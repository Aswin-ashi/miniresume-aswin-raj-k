from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
import uuid

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Resume Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/candidates")
async def upload_candidate(
    full_name: str = Form(...),
    dob: date = Form(...),
    contact_number: str = Form(...),
    address: str = Form(...),
    qualification: str = Form(...),
    graduation_year: int = Form(...),
    experience: float = Form(...),
    skills: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    ext = (".pdf", ".doc", ".docx")
    if not resume.filename.lower().endswith(ext):
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOC, or DOCX files are allowed"
        )

    cid = str(uuid.uuid4())

    candidate = models.Candidate(
        id=cid,
        full_name=full_name,
        dob=dob,
        contact_number=contact_number,
        address=address,
        qualification=qualification,
        graduation_year=graduation_year,
        experience=experience,
        skills=skills,
        resume_name=resume.filename
    )

    db.add(candidate)
    db.commit()

    return {"message": "Candidate added", "id": cid}


@app.get("/candidates")
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None,
    db: Session = Depends(get_db)
):

    query = db.query(models.Candidate)

    if skill:
        query = query.filter(models.Candidate.skills.contains(skill))

    if experience:
        query = query.filter(models.Candidate.experience >= experience)

    if graduation_year:
        query = query.filter(models.Candidate.graduation_year == graduation_year)

    return query.all()


@app.get("/candidates/{cid}")
def get_candidate(cid: str, db: Session = Depends(get_db)):

    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == cid
    ).first()

    if not candidate:
        raise HTTPException(404, "Candidate not found")

    return candidate


@app.delete("/candidates/{cid}")
def delete_candidate(cid: str, db: Session = Depends(get_db)):

    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == cid
    ).first()

    if not candidate:
        raise HTTPException(404, "Candidate not found")

    db.delete(candidate)
    db.commit()

    return {"message": "Candidate deleted"}