# API routes for email
from fastapi import APIRouter
from app.services.email_service import send_email

router = APIRouter()

@router.post("/send")
def send_test_email():
    success = send_email(
        to="candidate@example.com",
        subject="Interview Completed",
        body="Your AI interview session has been successfully recorded."
    )

    return {"status": "sent" if success else "failed"}
