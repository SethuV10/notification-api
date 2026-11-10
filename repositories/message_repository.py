
from .database import get_db_connection


class MessageRepository:

    def create(self, payload):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO messages
                (
                    room_id, category, staff_name, staff_id, team_id,
                    caller_name, caller_number, message_text, priority,
                    expires_at, requires_ack, acknowledged
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    int(payload.get("requires_ack", False)),
                    int(payload.get("acknowledged", False))
                ),
            )

            conn.commit()
            new_id = cursor.lastrowid

            return conn.execute(
                "SELECT * FROM messages WHERE id = ?",
                (new_id,)
            ).fetchone()

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_active_by_room(self, room_id: int):
        conn = get_db_connection()
        try:
            return conn.execute(
                """
                SELECT *
                FROM messages
                WHERE (room_id = ? OR room_id = 999)
                AND acknowledged = 0
                AND created_at >= date('now', 'localtime')
                AND created_at < datetime(date('now', 'localtime'), '+1 day')
                ORDER BY created_at DESC
                """,
                (room_id,),
            ).fetchall()
        finally:
            conn.close()

    def get_all_Active_messages(self):
        conn = get_db_connection()
        try:
            return conn.execute(
                """
                SELECT *
                FROM messages
                WHERE acknowledged = 0
                AND created_at >= datetime('now', '-10 days')
                ORDER BY created_at DESC
                """
            ).fetchall()
        finally:
            conn.close()

    def get_active_by_team(self, team_id: int):
        conn = get_db_connection()
        try:
            return conn.execute(
                """
                SELECT *
                FROM messages
                WHERE team_id = ? AND acknowledged = 0
                ORDER BY created_at DESC
                """,
                (team_id,),
            ).fetchall()
        finally:
            conn.close()

    def get_active_by_staff(self, staff_id: int):
        conn = get_db_connection()
        try:
            return conn.execute(
                """
                SELECT *
                FROM messages
                WHERE staff_id = ? AND acknowledged = 0
                ORDER BY created_at DESC
                """,
                (staff_id,),
            ).fetchall()
        finally:
            conn.close()

    def get_history(self):
        conn = get_db_connection()
        try:
            return conn.execute(
                "SELECT * FROM messages ORDER BY created_at DESC"
            ).fetchall()
        finally:
            conn.close()

    def acknowledge(self, message_id: int, acknowledged_at: str):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                UPDATE messages
                SET acknowledged = 1, acknowledged_at = ?
                WHERE id = ?
                """,
                (acknowledged_at, message_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    
    def set_requires_ack(self, message_id: int, requires_ack: bool):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                UPDATE messages
                SET requires_ack = ?
                WHERE id = ?
                """,
                (int(requires_ack), message_id),
            )

            conn.commit()
            return cursor.rowcount > 0

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

