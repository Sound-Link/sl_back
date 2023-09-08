# user_schema.py

from pydantic import BaseModel
from typing import Optional
from typing import List

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserList(BaseModel):
    users: List[User]
