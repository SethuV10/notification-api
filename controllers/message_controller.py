from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.message_service import MessageService
from controllers.auth_controller import get_current_user

router = APIRouter()
message_service = MessageService()


class MessageCreate(BaseModel):
    room_id: int
    staff_name: str = ""
    staff_id: int | None = None
    team_id: int | None = None
    caller_name: str | None = None
    caller_number: str | None = None
    message_text: str
    priority: str = "normal"
    category: str = "Call"
    acknowledged: bool = False
    requires_ack: bool = False

class AcknowledgeRequest(BaseModel):
    message_id: int


@router.post("/messages")
def create_message(message: MessageCreate, current_user: str = Depends(get_current_user)):
    payload = message.model_dump()

    print("ACKNOWLEDGED:", message.acknowledged)
    print("REQUIRES_ACK:", message.requires_ack)
    print("FULL PAYLOAD:", payload)

    payload["acknowledged"] = int(message.acknowledged)
    payload["requires_ack"] = int(message.requires_ack)

    return dict(message_service.create_message(payload))

@router.get("/messages/history")
def get_message_history(current_user: str = Depends(get_current_user)):
    return [dict(msg) for msg in message_service.list_history()]


@router.get("/messages/active/{room_id}")
def get_active_messages(room_id: int):
    return [dict(msg) for msg in message_service.list_active_messages(room_id)]

@router.get("/messages/active/team/{team_id}")
def get_active_messages_by_team(team_id: int):
    return [dict(msg) for msg in message_service.list_active_messages_by_team(team_id)]

@router.get("/messages/active/staff/{staff_id}")
def get_active_messages_by_staff(staff_id: int):
    return [dict(msg) for msg in message_service.list_active_messages_by_staff(staff_id)]
