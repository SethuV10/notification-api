from .database import get_db_connection


class CategoryRepository:
    def create(self, name: str, description: str | None = None):
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )
        conn.commit()
        new_id = cursor.lastrowid
        category = conn.execute("SELECT * FROM categories WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return category

    def list_categories(self):
        conn = get_db_connection()
        categories = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
        conn.close()
        return categories

    def get_by_id(self, category_id: int):
        conn = get_db_connection()
        category = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
        conn.close()
        return category

    def get_by_name(self, name: str):
        conn = get_db_connection()
        category = conn.execute("SELECT * FROM categories WHERE name = ?", (name,)).fetchone()
        conn.close()
        return category

    def update(self, category_id: int, name: str = None, description: str = None):
        conn = get_db_connection()
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if updates:
            params.append(category_id)
            query = f"UPDATE categories SET {', '.join(updates)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()

        category = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
        conn.close()
        return category

    def delete(self, category_id: int):
        conn = get_db_connection()
        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        conn.close()

    def exists(self, name: str) -> bool:
        conn = get_db_connection()
        exists = conn.execute("SELECT id FROM categories WHERE name = ?", (name,)).fetchone()
        conn.close()
        return exists is not None
