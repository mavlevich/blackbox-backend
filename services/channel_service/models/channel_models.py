from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from services.channel_service.db.database import Base


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
