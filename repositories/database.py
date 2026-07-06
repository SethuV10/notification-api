import sqlite3
from pathlib import Path

import bcrypt

DB_PATH = Path(__file__).resolve().parent.parent / "call_notifications.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            staff_id INTEGER UNIQUE,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            lastlogin TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (staff_id) REFERENCES staff(id)
        )
        """
    )
    existing_user_columns = [row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
    if "staff_id" not in existing_user_columns:
        conn.execute("ALTER TABLE users ADD COLUMN staff_id INTEGER")
    if "lastlogin" not in existing_user_columns:
        conn.execute("ALTER TABLE users ADD COLUMN lastlogin TEXT")
    if "active" not in existing_user_columns:
        conn.execute("ALTER TABLE users ADD COLUMN active INTEGER DEFAULT 1")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            room_id INTEGER NOT NULL,
            category TEXT DEFAULT 'Call',
            staff_name TEXT NOT NULL,
            staff_id INTEGER,
            team_id INTEGER,
            caller_name TEXT NOT NULL,
            caller_number TEXT,
            message_text TEXT NOT NULL,
            priority TEXT DEFAULT 'normal',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            expires_at TEXT,
            acknowledged INTEGER DEFAULT 0,
            acknowledged_at TEXT,
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (staff_id) REFERENCES staff(id),
            FOREIGN KEY (team_id) REFERENCES teams(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL,
            short_name TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY,
            staff_name TEXT NOT NULL,
            staff_short_name TEXT NOT NULL,
            room_id INTEGER,
            role_id INTEGER,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
        """
    )
    existing_staff_columns = [row[1] for row in conn.execute("PRAGMA table_info(staff)").fetchall()]
    if "role_id" not in existing_staff_columns:
        conn.execute("ALTER TABLE staff ADD COLUMN role_id INTEGER")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS staff_teams (
            id INTEGER PRIMARY KEY,
            staff_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (staff_id) REFERENCES staff(id),
            FOREIGN KEY (team_id) REFERENCES teams(id),
            UNIQUE(staff_id, team_id)
        )
        """
    )
    
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Hose')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Competition')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('IHC')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('SPP')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Transport')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Parent call-in')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Parent meet')")
    
    conn.execute("INSERT OR IGNORE INTO rooms (name, description) VALUES ('Floor1', 'First Floor Staff')")
    conn.execute("INSERT OR IGNORE INTO rooms (name, description) VALUES ('Floor2', 'Second Floor Staff')")
    conn.execute("INSERT OR IGNORE INTO rooms (name, description) VALUES ('Accounts', 'Accounts Department')")

    conn.execute("INSERT OR IGNORE INTO roles (name, description) VALUES ('HR', 'Human Resource')")
    conn.execute("INSERT OR IGNORE INTO roles (name, description) VALUES ('Admin', 'Admin')")
    conn.execute("INSERT OR IGNORE INTO roles (name, description) VALUES ('Principal', 'management')")
    conn.execute("INSERT OR IGNORE INTO roles (name, description) VALUES ('Staff', 'Teachers')")

    admin_role = conn.execute("SELECT id FROM roles WHERE name = 'Admin'").fetchone()

    admin_staff = conn.execute(
        "SELECT id FROM staff WHERE staff_name = 'Super Admin' AND staff_short_name = 'Admin' LIMIT 1"
    ).fetchone()
    if not admin_staff and admin_role:
        cursor = conn.execute(
            "INSERT INTO staff (staff_name, staff_short_name, role_id, active) VALUES (?, ?, ?, 1)",
            ("Super Admin", "Admin", admin_role[0]),
        )
        admin_staff_id = cursor.lastrowid
    elif admin_staff:
        admin_staff_id = admin_staff[0]
    else:
        admin_staff_id = None

    existing_admin = conn.execute("SELECT id, staff_id FROM users WHERE username = 'admin'").fetchone()
    if existing_admin:
        if admin_staff_id and not existing_admin[1]:
            conn.execute("UPDATE users SET staff_id = ? WHERE id = ?", (admin_staff_id, existing_admin[0]))
    else:
        hashed = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
        if admin_staff_id is None:
            raise RuntimeError("Unable to create default admin user because default staff record could not be created.")
        conn.execute(
            "INSERT INTO users (staff_id, username, password_hash, active) VALUES (?, ?, ?, 1)",
            (admin_staff_id, "admin", hashed),
        )
        print("✅ Default admin user created: username='admin', password='admin123'")

    conn.commit()
    conn.close()
