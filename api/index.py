from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os

app = FastAPI()

# Enable CORS (for testing in browser or external tools)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load student data from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'q-vercel-python.json')

with open(json_path, 'r') as f:
    students_data = json.load(f)

@app.get("/")
async def root():
    return {"message": "Student Marks API. Use /api?name=X&name=Y to get marks."}

@app.get("/api")
async def get_marks(name: Optional[List[str]] = Query(None)):
    """
    Get marks for one or more students.
    Example: /api?name=R&name=iRcVEjb
    """
    if not name:
        return {"error": "Please provide at least one name as a query parameter."}

    results = []
    for student_name in name:
        student = next(
            (s for s in students_data if s["name"].lower() == student_name.lower()),
            None
        )
        if student:
            results.append({"name": student_name, "marks": student["marks"]})
        else:
            results.append({"name": student_name, "marks": None})

    return {"results": results}

# For local testing via `python index.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
