from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    channel_id: int
    sender_id: int
    content: str


class MessageRead(BaseModel):
    id: int
    channel_id: int
    sender_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
