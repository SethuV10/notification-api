from fastapi import HTTPException
from repositories.team_repository import TeamRepository


class TeamService:
    def __init__(self, team_repository: TeamRepository | None = None):
        self.team_repository = team_repository or TeamRepository()

    def create_team(self, team_name: str, short_name: str):
        return self.team_repository.create(team_name, short_name)

    def list_teams(self):
        return self.team_repository.list_teams()

    def get_team(self, team_id: int):
        team = self.team_repository.get_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

    def update_team(self, team_id: int, team_name: str, short_name: str):
        team = self.team_repository.get_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return self.team_repository.update(team_id, team_name, short_name)

    def delete_team(self, team_id: int):
        team = self.team_repository.get_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        self.team_repository.delete(team_id)
        return {"status": "deleted", "team_id": team_id}
