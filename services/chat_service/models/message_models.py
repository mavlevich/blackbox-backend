from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from services.chat_service.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    sender_id = Column(Integer, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="messages")
