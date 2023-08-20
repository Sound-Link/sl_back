from fastapi import APIRouter, Depends, HTTPException, WebSocket, UploadFile, File
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from . import room_crud, room_schema
from database import get_db
from typing import List, Dict

from starlette.responses import FileResponse
import os

router = APIRouter()

@router.get("/rooms/{room_id}", response_model=room_schema.RoomInDB)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = room_crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.get("/rooms/", response_model=List[room_schema.RoomInDB])
def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rooms = room_crud.get_rooms(db, skip=skip, limit=limit)
    return rooms

@router.post("/rooms/", response_model=room_schema.RoomInDB)
def create_room(room: room_schema.RoomCreate, db: Session = Depends(get_db)):
    return room_crud.create_room(db=db, room=room)

@router.put("/rooms/{room_id}", response_model=room_schema.RoomInDB)
def update_room(room_id: int, room: room_schema.RoomUpdate, db: Session = Depends(get_db)):
    return room_crud.update_room(db=db, room=room, room_id=room_id)

@router.delete("/rooms/{room_id}", response_model=room_schema.RoomInDB)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_crud.delete_room(db=db, room_id=room_id)

# Dictionary to manage audio data for each room
rooms_audio_data: Dict[str, bytes] = {}

@router.websocket("/ws/voice/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    print(f"Accepted connection for room: {room_id}")

    while True:
        audio_data = await websocket.receive_bytes()

        # For demonstration purposes, we'll just print the length of the received audio data.
        # In a real-world scenario, you might process this data further.
        print(f"Received audio data of length {len(audio_data)} bytes for room: {room_id}")

# Define the path to save the text file
file_path = "received_text.txt"

@router.websocket("/ws/text/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"Accepted connection")

    while True:
        text_data = await websocket.receive_text()

        # Writing the received text data to a file
        with open(file_path, 'a') as file:  # 'a' mode appends data to the file
            file.write(text_data + "\n")  # Appending a newline for clarity

        print(f"Saved received text")

AUDIO_PATH = "audio_files"
# Ensure the directory exists
if not os.path.exists(AUDIO_PATH):
    os.makedirs(AUDIO_PATH)

@router.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_location = os.path.join(AUDIO_PATH, file.filename)
        with open(file_location, "wb+") as f:
            f.write(file.file.read())
        
        return {"status": "success", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving audio: {e}")

@router.get("/download/{filename}/")
async def download_audio(filename: str):
    file_location = os.path.join(AUDIO_PATH, filename)
    if not os.path.isfile(file_location):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    return FileResponse(file_location, headers={"Content-Disposition": f"attachment; filename={filename}"})