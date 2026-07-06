from .database import get_db_connection


class TeamRepository:
    def create(self, team_name: str, short_name: str):
        conn = get_db_connection()
        cursor = conn.execute(
            """
            INSERT INTO teams (team_name, short_name)
            VALUES (?, ?)
            """,
            (team_name, short_name),
        )
        conn.commit()
        new_id = cursor.lastrowid
        team = conn.execute("SELECT * FROM teams WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return team

    def list_teams(self):
        conn = get_db_connection()
        teams = conn.execute("SELECT * FROM teams ORDER BY team_name").fetchall()
        conn.close()
        return teams

    def get_by_id(self, team_id: int):
        conn = get_db_connection()
        team = conn.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
        conn.close()
        return team

    def update(self, team_id: int, team_name: str, short_name: str):
        conn = get_db_connection()
        conn.execute(
            "UPDATE teams SET team_name = ?, short_name = ? WHERE id = ?",
            (team_name, short_name, team_id),
        )
        conn.commit()
        team = conn.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
        conn.close()
        return team

    def delete(self, team_id: int):
        conn = get_db_connection()
        conn.execute("DELETE FROM teams WHERE id = ?", (team_id,))
        conn.commit()
        conn.close()
