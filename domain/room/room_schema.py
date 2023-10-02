from pydantic import BaseModel
from datetime import datetime

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    user_id: int

class RoomUpdate(RoomBase):
    pass

class RoomInDB(RoomBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
