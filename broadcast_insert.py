def broadcast_message(message):
    # Define the 6 rooms
    rooms = ["Accounts", "Floor1", "Floor2", "Floor3", "Floor5", "General"]
    
    # Loop through each room and broadcast
    for room in rooms:
        print(f"Broadcasting to {room}: {message}")

# Example usage
broadcast_message("Urgent callback needed regarding Project X")
