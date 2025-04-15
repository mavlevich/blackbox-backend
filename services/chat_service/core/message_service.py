from sqlalchemy.orm import Session
from shared.models.chat_models import Message
from datetime import datetime
from ..schemas.message_schemas import MessageCreate


def create_message(db: Session, message_data: MessageCreate) -> Message:
    message = Message(
        channel_id=message_data.channel_id,
        sender_id=message_data.sender_id,
        content=message_data.content,
        timestamp=datetime.utcnow()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
