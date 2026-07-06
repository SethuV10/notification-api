from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.user_service import UserService
from controllers.auth_controller import get_current_user

router = APIRouter()
user_service = UserService()


class UserCreate(BaseModel):
    staff_id: int
    username: str
    password: str
    active: int = 1


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/users")
def create_user(user: UserCreate, current_user: str = Depends(get_current_user)):
    return user_service.create_user(
        staff_id=user.staff_id,
        username=user.username,
        password=user.password,
        active=user.active,
    )


@router.put("/users/change-password")
def change_password(request: PasswordChangeRequest, current_user: str = Depends(get_current_user)):
    return user_service.change_password(current_user, request.current_password, request.new_password)


@router.get("/users")
def list_users(current_user: str = Depends(get_current_user)):
    return [dict(user) for user in user_service.list_users()]
