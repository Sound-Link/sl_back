from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)

class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    create_user_email = Column(String, ForeignKey('user.email'))
    
    creator = relationship("User", back_populates="rooms")
    chats = relationship("Chat", back_populates="room")

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    text = Column(String)
    user_type = Column(String)  # Assuming user_type is a String field
    room_id = Column(Integer, ForeignKey('room.id'))

    room = relationship("Room", back_populates="chats")

# Assuming a back relationship for User to Room
User.rooms = relationship("Room", back_populates="creator")
