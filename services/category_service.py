from fastapi import HTTPException
from repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository | None = None):
        self.category_repository = category_repository or CategoryRepository()

    def create_category(self, name: str, description: str | None = None):
        if self.category_repository.exists(name):
            raise HTTPException(status_code=400, detail="Category name already exists")
        return self.category_repository.create(name, description)

    def list_categories(self):
        return self.category_repository.list_categories()

    def get_category(self, category_id: int):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def get_category_by_name(self, name: str):
        category = self.category_repository.get_by_name(name)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def update_category(self, category_id: int, name: str = None, description: str = None):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        if name and name != category["name"] and self.category_repository.exists(name):
            raise HTTPException(status_code=400, detail="Category name already exists")
        return self.category_repository.update(category_id, name, description)

    def delete_category(self, category_id: int):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        self.category_repository.delete(category_id)
        return {"status": "deleted", "category_id": category_id}
