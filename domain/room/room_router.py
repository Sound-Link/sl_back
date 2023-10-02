from fastapi import APIRouter, Depends, HTTPException, WebSocket, UploadFile, File
from fastapi.responses import FileResponse
import io

from sqlalchemy.orm import Session
from . import room_crud, room_schema
from database import get_db
from typing import List, Dict

from speech_recognition import Recognizer, AudioData
import speech_recognition as sr
from starlette.responses import FileResponse
import os

router = APIRouter()

@router.post("/rooms/create/")
def create_room_by_email(room =  room_schema.RoomCreate,db: Session = Depends(get_db)):
    room = room_crud.create_room_by_user_and_email(db, email=room.email, name=room.name)
    return room

# @router.put("/rooms/{room_id}", response_model=room_schema.RoomInDB)
# def update_room(room_id: int, room: room_schema.RoomUpdate, db: Session = Depends(get_db)):
#     return room_crud.update_room(db=db, room=room, room_id=room_id)

@router.delete("/rooms/delete/{room_id}", response_model=room_schema.RoomInDB)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_crud.delete_room(db=db, room_id=room_id)

@router.get("/rooms/user/{email}/", response_model=List[room_schema.RoomInDB])
def read_rooms_by_email(email: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rooms = room_crud.get_rooms_by_email(db, email=email, skip=skip, limit=limit)
    return rooms






r = Recognizer()

# Dictionary to manage audio data for each room
rooms_audio_data: Dict[str, bytes] = {}

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
async def upload_audio(file: UploadFile = None):
    if not file:
        raise HTTPException(status_code=400, detail="파일이 제공되지 않았습니다.")

    try:
        # 오디오 파일을 직접 읽습니다.
        audio_bytes = file.file.read()

        # 오디오를 바로 인식합니다.
        text = recognize_audio(audio_bytes)
        return {"status": "success", "text": text}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{type(e).__name__}: {str(e)}")

def recognize_audio(audio_bytes: bytes) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='ko-KR')
    return text

@router.get("/download/{filename}/")
async def download_audio(filename: str):
    file_location = os.path.join(AUDIO_PATH, filename)
    if not os.path.isfile(file_location):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    return FileResponse(file_location, headers={"Content-Disposition": f"attachment; filename={filename}"})