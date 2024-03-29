from sqlalchemy.orm import Session
from models import Chat
from .chat_schema import ChatCreate, ChatUpdate

def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()

def get_chats_by_room(db: Session, room_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Chat)
        .filter(Chat.room_id == room_id)
        .order_by(Chat.created_at)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_chat(db: Session, room_id: int, text: str):
    chat = Chat(room_id=room_id, text=text)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def update_chat(db: Session, chat: ChatUpdate, chat_id: int):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    for key, value in chat.dict().items():
        setattr(db_chat, key, value)
    db.commit()
    return db_chat

def delete_chat(db: Session, chat_id: int):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    db.delete(db_chat)
    db.commit()
    return db_chat
