from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.category_service import CategoryService
from controllers.auth_controller import get_current_user

router = APIRouter()
category_service = CategoryService()


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


@router.post("/categories")
def create_category(category: CategoryCreate, current_user: str = Depends(get_current_user)):
    return dict(category_service.create_category(category.name, category.description))


@router.get("/categories")
def list_categories():
    return [dict(cat) for cat in category_service.list_categories()]


@router.get("/categories/name/{name}")
def get_category_by_name(name: str):
    return dict(category_service.get_category_by_name(name))


@router.get("/categories/{category_id}")
def get_category(category_id: int):
    return dict(category_service.get_category(category_id))


@router.put("/categories/{category_id}")
def update_category(category_id: int, category: CategoryUpdate, current_user: str = Depends(get_current_user)):
    return dict(category_service.update_category(category_id, category.name, category.description))


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, current_user: str = Depends(get_current_user)):
    return category_service.delete_category(category_id)
