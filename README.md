## Mini Resume Management API 

A lightweight FastAPI REST API for uploading, filtering, and managing candidate resumes

## Python Version ##
Python 3.13

## Installation ##

# 1. Clone Repository
git clone https://github.com/Aswin-ashi/miniresume-aswin-raj-k.git

cd miniresume-aswin-raj-k

# 2. Install Dependencies
pip install -r requirements.txt

## Run Application
python -m uvicorn main:app --reload

## open browser
http://127.0.0.1:8000/docs

## API Endpoints

## Health Check
GET /health

## Upload Candidate
POST /candidates  
Form-Data:
- full_name
- dob
- contact_number
- address
- qualification
- graduation_year
- experience
- skills (comma separated)
- resume (file)

### List Candidates
GET /candidates?skill=python&experience=1&graduation_year=2024

### Get Candidate
GET /candidates/{id}

### Delete Candidate
DELETE /candidates/{id}
