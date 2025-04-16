from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.db.database import Base



class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_group = Column(Boolean, default=False)

    messages = relationship("Message", back_populates="channel")
    participants = relationship("ChannelParticipant", back_populates="channel")


class ChannelParticipant(Base):
    __tablename__ = "channel_participants"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    user_id = Column(Integer, index=True)

    channel = relationship("Channel", back_populates="participants")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    sender_id = Column(Integer, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="messages")
