# API routes for sessions
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.interview_session import InterviewSession

router = APIRouter()

# In-memory store (replace with DB later)
ACTIVE_SESSIONS = {}


@router.post("/start")
def start_session(candidate_id: str):
    """
    Start a new interview session for a candidate.
    """
    if candidate_id in ACTIVE_SESSIONS:
        raise HTTPException(status_code=400, detail="Session already active")

    session = InterviewSession(
        candidate_id=candidate_id,
        start_time=datetime.utcnow(),
        status="active"
    )

    ACTIVE_SESSIONS[candidate_id] = session
    return {"message": "Session started", "session": session}


@router.post("/end")
def end_session(candidate_id: str):
    """
    End an active interview session.
    """
    if candidate_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="No active session found")

    session = ACTIVE_SESSIONS.pop(candidate_id)
    session.status = "completed"

    return {"message": "Session ended", "session": session}


@router.get("/status")
def session_status(candidate_id: str):
    """
    Check session status.
    """
    session = ACTIVE_SESSIONS.get(candidate_id)
    if not session:
        return {"status": "no active session"}

    return {"status": session.status, "started_at": session.start_time}
