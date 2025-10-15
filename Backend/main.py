# backend/main.py
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
# Support both package-relative imports (when run as a package) and absolute imports
# (when running scripts or tests from the Backend directory). This avoids
# ModuleNotFoundError in different execution contexts (uvicorn, tests, Render).
try:
    from .llm_client import generate_diagnosis
    from .db import init_db, save_query, get_history
except Exception:
    # Fallback to absolute imports when the package context is not present
    from llm_client import generate_diagnosis
    from db import init_db, save_query, get_history
import os

app = FastAPI(title="Healthcare Symptom Checker API")

# Allow local frontend (Streamlit) to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class DiagnoseRequest(BaseModel):
    text: str
    user_id: Optional[str] = None


@app.post("/api/diagnose")
async def diagnose(req: DiagnoseRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="No symptoms provided")

    # Call LLM (or fallback) synchronously; it's quick for our use case
    response = generate_diagnosis(req.text)
    try:
        save_query(req.user_id, req.text, response)
    except Exception:
        # Don't fail the request if logging fails
        pass

    return {"result": response, "disclaimer": "Educational purpose only. Not a medical diagnosis."}


@app.get("/api/logs")
async def get_logs():
    # Return latest 10 logs
    try:
        conn = sqlite3.connect(os.getenv("DB_PATH", "symptom_history.db"))
        c = conn.cursor()
        c.execute("SELECT id, symptoms, response, created_at FROM history ORDER BY id DESC LIMIT 10")
        rows = c.fetchall()
        conn.close()

        return {"logs": [{"id": r[0], "symptom": r[1], "response": r[2], "created_at": r[3]} for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

