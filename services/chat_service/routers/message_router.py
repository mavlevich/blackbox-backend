from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.chat_service.schemas.message_schemas import MessageCreate, MessageRead
from ..core.message_service import create_message
from services.chat_service.db.database import get_db

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/send", response_model=MessageRead)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db, message)
