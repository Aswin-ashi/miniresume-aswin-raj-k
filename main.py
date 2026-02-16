from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
from datetime import date
import uuid

app = FastAPI(title="Mini Resume Management API")

db = {}

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
    resume: UploadFile = File(...)
):
    ext=('.pdf', '.doc', '.docx')
    if not resume.filename.lower().endswith(ext):
        raise HTTPException(status_code=400, detail="Only PDF, DOC, or DOCX files are allowed")
    
    cid = str(uuid.uuid4())

    db[cid] = {
        "id": cid,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "address": address,
        "qualification": qualification,
        "graduation_year": graduation_year,
        "experience": experience,
        "skills": skills.split(","),
        "resume_name": resume.filename
    }

    return {"message": "Candidate added", "id": cid}

@app.get("/candidates")
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None
):
    result = list(db.values())

    if skill:
        result = [c for c in result if skill.lower() in [s.lower() for s in c["skills"]]]

    if experience:
        result = [c for c in result if c["experience"] >= experience]

    if graduation_year:
        result = [c for c in result if c["graduation_year"] == graduation_year]

    return result

@app.get("/candidates/{cid}")
def get_candidate(cid: str):
    if cid not in db:
        raise HTTPException(404, "Candidate not found")
    return db[cid]

@app.delete("/candidates/{cid}")
def delete_candidate(cid: str):
    if cid not in db:
        raise HTTPException(404, "Candidate not found")
    del db[cid]
    return {"message": "Candidate deleted"}
