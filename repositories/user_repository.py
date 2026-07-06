import bcrypt

from .database import get_db_connection


class UserRepository:
    def get_by_username(self, username: str):
        conn = get_db_connection()
        user = conn.execute(
            """
            SELECT u.id, u.staff_id, u.username, u.password_hash, u.lastlogin, u.active, s.role_id
            FROM users u
            LEFT JOIN staff s ON u.staff_id = s.id
            WHERE u.username = ?
            """,
            (username,),
        ).fetchone()
        conn.close()
        return user

    def list_users(self):
        conn = get_db_connection()
        users = conn.execute(
            """
            SELECT u.id, u.staff_id, u.username, u.lastlogin, u.active, s.role_id, s.staff_name as staff_name
            FROM users u
            LEFT JOIN staff s ON u.staff_id = s.id
            ORDER BY u.username
            """
        ).fetchall()
        conn.close()
        return users

    def exists(self, username: str) -> bool:
        conn = get_db_connection()
        exists = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return exists is not None

    def create(self, staff_id: int, username: str, password: str, active: int = 1):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO users (staff_id, username, password_hash, active)
            VALUES (?, ?, ?, ?)
            """,
            (staff_id, username, hashed, active),
        )
        conn.commit()
        new_id = cursor.lastrowid
        new_user = conn.execute("SELECT id, staff_id, username, lastlogin, active FROM users WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return new_user

    def update_password(self, username: str, password_hash: bytes):
        conn = get_db_connection()
        conn.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
        conn.commit()
        conn.close()

    def update_lastlogin(self, username: str, lastlogin: str):
        conn = get_db_connection()
        conn.execute("UPDATE users SET lastlogin = ? WHERE username = ?", (lastlogin, username))
        conn.commit()
        conn.close()
