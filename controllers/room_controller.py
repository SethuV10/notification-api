from fastapi import APIRouter, Depends
from pydantic import BaseModel

from controllers.auth_controller import get_current_user
from services.room_service import RoomService

router = APIRouter()
room_service = RoomService()


class RoomCreate(BaseModel):
    name: str
    description: str | None = None


class RoomUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


@router.post("/rooms")
def create_room(room: RoomCreate, current_user: str = Depends(get_current_user)):
    return dict(room_service.create_room(room.name, room.description))


@router.get("/rooms")
def list_rooms():
    return [dict(room) for room in room_service.list_rooms()]


@router.get("/rooms/{room_id}")
def get_room(room_id: int):
    return dict(room_service.get_room(room_id))


@router.put("/rooms/{room_id}")
def update_room(room_id: int, room: RoomUpdate, current_user: str = Depends(get_current_user)):
    return dict(room_service.update_room(room_id, room.name, room.description))


@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, current_user: str = Depends(get_current_user)):
    return room_service.delete_room(room_id)
