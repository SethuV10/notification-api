from fastapi import HTTPException
from repositories.staff_repository import StaffRepository


class StaffService:
    def __init__(self, staff_repository: StaffRepository | None = None):
        self.staff_repository = staff_repository or StaffRepository()

    def create_staff(self, staff_name: str, staff_short_name: str, room_id: int, role_id: int | None = None):
        return self.staff_repository.create(staff_name, staff_short_name, room_id, role_id)

    def list_staff(self):
        return self.staff_repository.list_staff()

    def get_staff(self, staff_id: int):
        staff = self.staff_repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        return staff

    def get_staff_by_room(self, room_id: int):
        return self.staff_repository.get_by_room(room_id)

    def update_staff(self, staff_id: int, staff_name: str = None, staff_short_name: str = None, room_id: int = None, role_id: int | None = None, active: int = None):
        staff = self.staff_repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        return self.staff_repository.update(staff_id, staff_name, staff_short_name, room_id, role_id, active)

    def delete_staff(self, staff_id: int):
        staff = self.staff_repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        self.staff_repository.delete(staff_id)
        return {"status": "deleted", "staff_id": staff_id}

    def add_staff_to_team(self, staff_id: int, team_id: int):
        staff = self.staff_repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        self.staff_repository.add_to_team(staff_id, team_id)
        return {"status": "added", "staff_id": staff_id, "team_id": team_id}

    def remove_staff_from_team(self, staff_id: int, team_id: int):
        staff = self.staff_repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        self.staff_repository.remove_from_team(staff_id, team_id)
        return {"status": "removed", "staff_id": staff_id, "team_id": team_id}

    def get_staff_teams(self, staff_id: int):
        staff = self.staff_repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        return self.staff_repository.get_teams(staff_id)

    def get_team_staff(self, team_id: int):
        return self.staff_repository.get_staff_by_team(team_id)
