from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.staff_service import StaffService
from controllers.auth_controller import get_current_user

router = APIRouter()
staff_service = StaffService()


class StaffCreate(BaseModel):
    staff_name: str
    staff_short_name: str
    room_id: int
    role_id: int | None = None


class StaffUpdate(BaseModel):
    staff_name: str | None = None
    staff_short_name: str | None = None
    room_id: int | None = None
    role_id: int | None = None
    active: int | None = None


class StaffTeamRequest(BaseModel):
    team_id: int


class StaffResponse(BaseModel):
    id: int
    staff_name: str
    staff_short_name: str
    room_id: int | None
    role_id: int | None
    active: int
    created_at: str

    class Config:
        from_attributes = True


@router.post("/staff")
def create_staff(staff: StaffCreate, current_user: str = Depends(get_current_user)):
    return dict(staff_service.create_staff(
        staff.staff_name,
        staff.staff_short_name,
        staff.room_id,
        staff.role_id
    ))


@router.get("/staff", response_model=list[StaffResponse])
def list_staff():
    return [dict(s) for s in staff_service.list_staff()]


@router.get("/staff/room/{room_id}", response_model=list[StaffResponse])
def get_staff_by_room(room_id: int):
    return [dict(s) for s in staff_service.get_staff_by_room(room_id)]


@router.get("/staff/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int):
    return dict(staff_service.get_staff(staff_id))


@router.get("/staff/{staff_id}/teams")
def get_staff_teams(staff_id: int):
    return [dict(team) for team in staff_service.get_staff_teams(staff_id)]


@router.get("/teams/{team_id}/staff")
def get_team_staff(team_id: int):
    return [dict(s) for s in staff_service.get_team_staff(team_id)]

def update_staff(staff_id: int, staff: StaffUpdate, current_user: str = Depends(get_current_user)):
    return dict(staff_service.update_staff(
        staff_id,
        staff.staff_name,
        staff.staff_short_name,
        staff.room_id,
        staff.role_id,
        staff.active
    ))


@router.delete("/staff/{staff_id}")
def delete_staff(staff_id: int, current_user: str = Depends(get_current_user)):
    return staff_service.delete_staff(staff_id)


@router.post("/staff/{staff_id}/teams")
def add_staff_to_team(staff_id: int, request: StaffTeamRequest, current_user: str = Depends(get_current_user)):
    return staff_service.add_staff_to_team(staff_id, request.team_id)


@router.delete("/staff/{staff_id}/teams/{team_id}")
def remove_staff_from_team(staff_id: int, team_id: int, current_user: str = Depends(get_current_user)):
    return staff_service.remove_staff_from_team(staff_id, team_id)


@router.get("/staff/{staff_id}/teams")
def get_staff_teams(staff_id: int):
    return [dict(team) for team in staff_service.get_staff_teams(staff_id)]


@router.get("/teams/{team_id}/staff")
def get_team_staff(team_id: int):
    return [dict(s) for s in staff_service.get_team_staff(team_id)]
