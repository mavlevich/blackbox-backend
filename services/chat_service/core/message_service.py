from sqlalchemy.orm import Session
from shared.models.chat_models import Message
from shared.schemas.chat_schemas import MessageCreate, MessageRead
from services.chat_service.core.encryption import encrypt_message, decrypt_message
from datetime import datetime


def create_message(db: Session, message: MessageCreate) -> MessageRead:
    encrypted = encrypt_message(message.content, message.password)

    db_message = Message(
        sender_id=message.sender_id,
        channel_id=message.channel_id,
        content=encrypted,
        timestamp=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return MessageRead(
        id=db_message.id,
        sender_id=db_message.sender_id,
        receiver_id=message.receiver_id,
        channel_id=db_message.channel_id,
        content=message.content,
        timestamp=db_message.timestamp
    )


def get_messages_for_channel(
    db: Session, channel_id: int, password: str
) -> list[MessageRead]:
    messages = db.query(Message).filter(Message.channel_id == channel_id).all()
    result = []
    for msg in messages:
        try:
            decrypted = decrypt_message(msg.content, password)
        except Exception:
            decrypted = "[Unable to decrypt]"

        result.append(MessageRead(
            id=msg.id,
            sender_id=msg.sender_id,
            receiver_id=None,
            channel_id=msg.channel_id,
            content=decrypted,
            timestamp=msg.timestamp
        ))
    return result
