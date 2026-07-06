from .database import get_db_connection


class RoleRepository:
    def create(self, name: str, description: str | None = None):
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO roles (name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )
        conn.commit()
        new_id = cursor.lastrowid
        role = conn.execute("SELECT * FROM roles WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return role

    def list_roles(self):
        conn = get_db_connection()
        roles = conn.execute("SELECT * FROM roles ORDER BY name").fetchall()
        conn.close()
        return roles

    def get_by_id(self, role_id: int):
        conn = get_db_connection()
        role = conn.execute("SELECT * FROM roles WHERE id = ?", (role_id,)).fetchone()
        conn.close()
        return role

    def get_by_name(self, name: str):
        conn = get_db_connection()
        role = conn.execute("SELECT * FROM roles WHERE name = ?", (name,)).fetchone()
        conn.close()
        return role

    def update(self, role_id: int, name: str = None, description: str = None):
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
            params.append(role_id)
            query = f"UPDATE roles SET {', '.join(updates)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()

        role = conn.execute("SELECT * FROM roles WHERE id = ?", (role_id,)).fetchone()
        conn.close()
        return role

    def delete(self, role_id: int):
        conn = get_db_connection()
        conn.execute("DELETE FROM roles WHERE id = ?", (role_id,))
        conn.commit()
        conn.close()

    def exists(self, name: str) -> bool:
        conn = get_db_connection()
        exists = conn.execute("SELECT id FROM roles WHERE name = ?", (name,)).fetchone()
        conn.close()
        return exists is not None
