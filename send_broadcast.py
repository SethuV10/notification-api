import sqlite3
from datetime import datetime

def broadcast_message(message, category="Competition", priority="normal"):
    conn = sqlite3.connect("call_notifications.db")
    cursor = conn.cursor()

    # Map room IDs to names
    room_map = {
        0: "General",
        1: "Floor1",
        2: "Floor2",
        3: "Floor3",
        4: "Accounts",
        5: "Floor5"
    }

    for room_id, room_name in room_map.items():
        cursor.execute("""
            INSERT INTO messages (room_id, category, staff_name, staff_id, message_text, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (room_id, category, "Sethu Valliyappan", 4, message, priority))
        
        # Console feedback with room name
        print(f"Inserted message into {room_name} (room_id {room_id})")

    conn.commit()
    conn.close()

# Example usage
broadcast_message("Urgent callback needed regarding Project X", category="Competition", priority="urgent")


