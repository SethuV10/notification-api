from .database import get_db_connection


class RoomRepository:
    def create(self, name: str, description: str | None = None):
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO rooms (name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )
        conn.commit()
        new_id = cursor.lastrowid
        room = conn.execute("SELECT * FROM rooms WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return room

    def list_rooms(self):
        conn = get_db_connection()
        rooms = conn.execute("SELECT * FROM rooms ORDER BY name").fetchall()
        conn.close()
        return rooms

    def get_by_id(self, room_id: int):
        conn = get_db_connection()
        room = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
        conn.close()
        return room

    def update(self, room_id: int, name: str | None = None, description: str | None = None):
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
            params.append(room_id)
            query = f"UPDATE rooms SET {', '.join(updates)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()

        room = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
        conn.close()
        return room

    def delete(self, room_id: int):
        conn = get_db_connection()
        conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
        conn.commit()
        conn.close()

    def exists(self, name: str) -> bool:
        conn = get_db_connection()
        exists = conn.execute("SELECT id FROM rooms WHERE name = ?", (name,)).fetchone()
        conn.close()
        return exists is not None
