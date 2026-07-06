from .database import get_db_connection


class StaffRepository:
    def create(self, staff_name: str, staff_short_name: str, room_id: int, role_id: int | None = None, active: int = 1):
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO staff (staff_name, staff_short_name, room_id, role_id, active)
            VALUES (?, ?, ?, ?, ?)
            """,
            (staff_name, staff_short_name, room_id, role_id, active),
        )
        conn.commit()
        new_id = cursor.lastrowid
        staff = conn.execute("SELECT * FROM staff WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return staff

    def list_staff(self):
        conn = get_db_connection()
        staff = conn.execute("SELECT * FROM staff ORDER BY staff_name").fetchall()
        conn.close()
        return staff

    def get_by_id(self, staff_id: int):
        conn = get_db_connection()
        staff = conn.execute("SELECT * FROM staff WHERE id = ?", (staff_id,)).fetchone()
        conn.close()
        return staff

    def get_by_room(self, room_id: int):
        conn = get_db_connection()
        staff = conn.execute("SELECT * FROM staff WHERE room_id = ? AND active = 1 ORDER BY staff_name", (room_id,)).fetchall()
        conn.close()
        return staff

    def update(self, staff_id: int, staff_name: str = None, staff_short_name: str = None, room_id: int = None, role_id: int | None = None, active: int = None):
        conn = get_db_connection()
        updates = []
        params = []
        if staff_name is not None:
            updates.append("staff_name = ?")
            params.append(staff_name)
        if staff_short_name is not None:
            updates.append("staff_short_name = ?")
            params.append(staff_short_name)
        if room_id is not None:
            updates.append("room_id = ?")
            params.append(room_id)
        if role_id is not None:
            updates.append("role_id = ?")
            params.append(role_id)
        if active is not None:
            updates.append("active = ?")
            params.append(active)

        if updates:
            params.append(staff_id)
            query = f"UPDATE staff SET {', '.join(updates)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()

        staff = conn.execute("SELECT * FROM staff WHERE id = ?", (staff_id,)).fetchone()
        conn.close()
        return staff

    def delete(self, staff_id: int):
        conn = get_db_connection()
        conn.execute("DELETE FROM staff_teams WHERE staff_id = ?", (staff_id,))
        conn.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
        conn.commit()
        conn.close()

    def add_to_team(self, staff_id: int, team_id: int):
        conn = get_db_connection()
        conn.execute(
            """
            INSERT OR IGNORE INTO staff_teams (staff_id, team_id)
            VALUES (?, ?)
            """,
            (staff_id, team_id),
        )
        conn.commit()
        conn.close()

    def remove_from_team(self, staff_id: int, team_id: int):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM staff_teams WHERE staff_id = ? AND team_id = ?",
            (staff_id, team_id),
        )
        conn.commit()
        conn.close()

    def get_teams(self, staff_id: int):
        conn = get_db_connection()
        teams = conn.execute(
            """
            SELECT t.* FROM teams t
            JOIN staff_teams st ON t.id = st.team_id
            WHERE st.staff_id = ?
            """,
            (staff_id,),
        ).fetchall()
        conn.close()
        return teams

    def get_staff_by_team(self, team_id: int):
        conn = get_db_connection()
        staff = conn.execute(
            """
            SELECT s.* FROM staff s
            JOIN staff_teams st ON s.id = st.staff_id
            WHERE st.team_id = ?
            ORDER BY s.staff_name
            """,
            (team_id,),
        ).fetchall()
        conn.close()
        return staff
