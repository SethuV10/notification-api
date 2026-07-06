from .database import get_db_connection


class MessageRepository:
    def create(self, payload):
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO messages
            (room_id, category, staff_name, staff_id, team_id, caller_name, caller_number, message_text, priority, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["room_id"],
                payload["category"],
                payload["staff_name"],
                payload["staff_id"],
                payload["team_id"],
                payload["caller_name"],
                payload["caller_number"],
                payload["message_text"],
                payload["priority"],
                payload["expires_at"],
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        new_msg = conn.execute("SELECT * FROM messages WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return new_msg

    def get_active_by_room(self, room_id: int):
        conn = get_db_connection()
        messages = conn.execute("""
                                SELECT *
                                FROM messages
                                WHERE room_id = ?
                                AND created_at >= date('now', 'localtime')
                                AND created_at < datetime(date('now', 'localtime'), '+1 day')
                                ORDER BY created_at DESC
                                """, (room_id,)).fetchall()
        conn.close()
        return messages
    
    def get_active_by_team(self, team_id: int):
        conn = get_db_connection()
        messages = conn.execute(
            "SELECT * FROM messages WHERE team_id = ? AND acknowledged = 0 ORDER BY created_at DESC",
            (team_id,),
        ).fetchall()
        conn.close()
        return messages
    
    def get_active_by_staff(self, staff_id: int):
        conn = get_db_connection()
        messages = conn.execute(
            "SELECT * FROM messages WHERE staff_id = ? AND acknowledged = 0 ORDER BY created_at DESC",
            (staff_id,),
        ).fetchall()
        conn.close()
        return messages


    def get_history(self):
        conn = get_db_connection()
        messages = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
        conn.close()
        return messages

    def acknowledge(self, message_id: int, acknowledged_at: str):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE messages
            SET acknowledged = 1, acknowledged_at = ?
            WHERE id = ?
            """,
            (acknowledged_at, message_id),
        )
        conn.commit()
        conn.close()
        return message_id
