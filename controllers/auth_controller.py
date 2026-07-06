from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from services.auth_service import AuthService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
auth_service = AuthService()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate(form_data.username, form_data.password)
    role_id = user["role_id"] if user and "role_id" in user.keys() else None
    token = auth_service.create_access_token(user["username"], role_id)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    return auth_service.verify_token(token)
