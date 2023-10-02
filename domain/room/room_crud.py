from sqlalchemy.orm import Session
from models import Room
from .room_schema import RoomCreate, RoomUpdate

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Room).offset(skip).limit(limit).all()

def create_room_by_user_and_email(db: Session, email: str, name: str):
    db_room = Room(name=name, create_user_email=email)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms_by_email(db: Session, email: str, skip: int = 0, limit: int = 10):
    return db.query(Room).filter(Room.create_user_email == email).offset(skip).limit(limit).all()

def update_room(db: Session, room: RoomUpdate, room_id: int):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    for key, value in room.dict().items():
        setattr(db_room, key, value)
    db.commit()
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    db.delete(db_room)
    db.commit()
    return db_room

def get_rooms_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Room).filter(Room.create_user_id == user_id).offset(skip).limit(limit).all()

