from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.role_service import RoleService
from controllers.auth_controller import get_current_user

router = APIRouter()
role_service = RoleService()


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


@router.post("/roles")
def create_role(role: RoleCreate, current_user: str = Depends(get_current_user)):
    return dict(role_service.create_role(role.name, role.description))


@router.get("/roles")
def list_roles():
    return [dict(r) for r in role_service.list_roles()]


@router.get("/roles/name/{name}")
def get_role_by_name(name: str):
    return dict(role_service.get_role_by_name(name))


@router.get("/roles/{role_id}")
def get_role(role_id: int):
    return dict(role_service.get_role(role_id))


@router.put("/roles/{role_id}")
def update_role(role_id: int, role: RoleUpdate, current_user: str = Depends(get_current_user)):
    return dict(role_service.update_role(role_id, role.name, role.description))


@router.delete("/roles/{role_id}")
def delete_role(role_id: int, current_user: str = Depends(get_current_user)):
    return role_service.delete_role(role_id)
