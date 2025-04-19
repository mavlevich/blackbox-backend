from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from services.chat_service.db.database import get_db
from shared.models.chat_models import Message
from shared.schemas.chat_schemas import MessageCreate, MessageRead
from services.chat_service.core.encryption import encrypt_message, decrypt_message
from datetime import datetime

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/send", response_model=MessageRead)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    try:
        encrypted = encrypt_message(message.content, message.password)

        db_message = Message(
            sender_id=message.sender_id,
            channel_id=message.channel_id,
            content=encrypted,
            timestamp=datetime.utcnow(),
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return MessageRead(
            id=db_message.id,
            sender_id=db_message.sender_id,
            channel_id=db_message.channel_id,
            content=message.content,
            timestamp=db_message.timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")


@router.get("/{channel_id}", response_model=list[MessageRead])
def get_messages(
    channel_id: int,
    password: str = Query(...),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(Message.channel_id == channel_id).all()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this channel.")

    result = []
    for msg in messages:
        try:
            decrypted = decrypt_message(msg.content, password)
        except Exception:
            decrypted = "[Unable to decrypt]"

        result.append(MessageRead(
            id=msg.id,
            sender_id=msg.sender_id,
            channel_id=msg.channel_id,
            content=decrypted,
            timestamp=msg.timestamp
        ))
    return result
