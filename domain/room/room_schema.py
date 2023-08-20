from pydantic import BaseModel
from datetime import datetime

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomInDB(RoomBase):
    id: int
    created_at: datetime
    create_user_id: int

    class Config:
        orm_mode = True