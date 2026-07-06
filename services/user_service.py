import bcrypt
from fastapi import HTTPException

from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()

    def create_user(self, staff_id: int, username: str, password: str, active: int = 1):
        if self.user_repository.exists(username):
            raise HTTPException(status_code=400, detail="Username already exists")
        return self.user_repository.create(staff_id, username, password, active)

    def list_users(self):
        return self.user_repository.list_users()

    def change_password(self, username: str, current_password: str, new_password: str):
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not bcrypt.checkpw(current_password.encode("utf-8"), user["password_hash"]):
            raise HTTPException(status_code=403, detail="Current password is incorrect")
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        self.user_repository.update_password(username, hashed)
        return {"status": "password changed"}
