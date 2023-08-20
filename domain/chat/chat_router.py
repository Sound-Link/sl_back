from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import chat_crud, chat_schema
from database import get_db
from typing import List

router = APIRouter()

@router.get("/chats/{chat_id}", response_model=chat_schema.ChatInDB)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = chat_crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@router.get("/chats/room/{room_id}", response_model=List[chat_schema.ChatInDB])
def read_chats_by_room(room_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    chats = chat_crud.get_chats_by_room(db, room_id=room_id, skip=skip, limit=limit)
    return chats

@router.post("/chats/", response_model=chat_schema.ChatInDB)
def create_chat(chat: chat_schema.ChatCreate, db: Session = Depends(get_db)):
    return chat_crud.create_chat(db=db, chat=chat)

@router.put("/chats/{chat_id}", response_model=chat_schema.ChatInDB)
def update_chat(chat_id: int, chat: chat_schema.ChatUpdate, db: Session = Depends(get_db)):
    return chat_crud.update_chat(db=db, chat=chat, chat_id=chat_id)

@router.delete("/chats/{chat_id}", response_model=chat_schema.ChatInDB)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    return chat_crud.delete_chat(db=db, chat_id=chat_id)
