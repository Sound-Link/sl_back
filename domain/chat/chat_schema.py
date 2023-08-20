from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    text: str
    user_type: str
    room_id: int

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    pass

class ChatInDB(ChatBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
