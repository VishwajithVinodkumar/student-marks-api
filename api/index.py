from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load JSON from the same folder (api/)
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'q-vercel-python.json')

with open(json_path, 'r') as f:
    students_data = json.load(f)

@app.get("/")
async def root():
    return {"message": "Student Marks API. Use /api?name=X&name=Y to get marks."}

@app.get("/api")
async def get_marks(name: Optional[List[str]] = Query(None)):
    if not name:
        return {"error": "Please provide at least one name as a query parameter."}

    results = []
    for student_name in name:
        student = next((s for s in students_data if s["name"].lower() == student_name.lower()), None)
        results.append({
            "name": student_name,
            "marks": student["marks"] if student else None
        })

    return {"results": results}
