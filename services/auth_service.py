import jwt
from datetime import datetime as dt, timedelta
from fastapi import HTTPException
import bcrypt

from repositories.user_repository import UserRepository

SECRET_KEY = "your-super-secret-key-change-this-in-production-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480


class AuthService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()

    def authenticate(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        if user["active"] != 1:
            raise HTTPException(status_code=403, detail="User account is not active")
        self.user_repository.update_lastlogin(username, dt.utcnow().isoformat())
        return user

    def create_access_token(self, username: str, role_id: int | None = None):
        expire = dt.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": username, "exp": expire}
        if role_id is not None:
            payload["role_id"] = role_id
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=401, detail="Invalid token") from exc
