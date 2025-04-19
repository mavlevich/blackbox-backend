from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    channel_id: int
    content: str
    password: str


class MessageRead(BaseModel):
    id: int
    sender_id: UUID
    receiver_id: UUID
    channel_id: int
    content: str  # decrypted
    timestamp: datetime

    class Config:
        orm_mode = True
