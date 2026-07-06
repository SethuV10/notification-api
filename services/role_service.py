from fastapi import HTTPException
from repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository | None = None):
        self.role_repository = role_repository or RoleRepository()

    def create_role(self, name: str, description: str | None = None):
        if self.role_repository.exists(name):
            raise HTTPException(status_code=400, detail="Role name already exists")
        return self.role_repository.create(name, description)

    def list_roles(self):
        return self.role_repository.list_roles()

    def get_role(self, role_id: int):
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def get_role_by_name(self, name: str):
        role = self.role_repository.get_by_name(name)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def update_role(self, role_id: int, name: str = None, description: str = None):
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        if name and name != role["name"] and self.role_repository.exists(name):
            raise HTTPException(status_code=400, detail="Role name already exists")
        return self.role_repository.update(role_id, name, description)

    def delete_role(self, role_id: int):
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        self.role_repository.delete(role_id)
        return {"status": "deleted", "role_id": role_id}
