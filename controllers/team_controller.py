from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.team_service import TeamService
from controllers.auth_controller import get_current_user

router = APIRouter()
team_service = TeamService()


class TeamCreate(BaseModel):
    team_name: str
    short_name: str


class TeamUpdate(BaseModel):
    team_name: str | None = None
    short_name: str | None = None


class TeamResponse(BaseModel):
    id: int
    team_name: str
    short_name: str
    created_at: str

    class Config:
        from_attributes = True


@router.post("/teams")
def create_team(team: TeamCreate, current_user: str = Depends(get_current_user)):
    return dict(team_service.create_team(team.team_name, team.short_name))


@router.get("/teams", response_model=list[TeamResponse])
def list_teams():
    return [dict(team) for team in team_service.list_teams()]


@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int):
    return dict(team_service.get_team(team_id))


@router.put("/teams/{team_id}")
def update_team(team_id: int, team: TeamUpdate, current_user: str = Depends(get_current_user)):
    return dict(team_service.update_team(
        team_id,
        team.team_name or None,
        team.short_name or None
    ))


@router.delete("/teams/{team_id}")
def delete_team(team_id: int, current_user: str = Depends(get_current_user)):
    return team_service.delete_team(team_id)
