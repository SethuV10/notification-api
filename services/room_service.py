from repositories.room_repository import RoomRepository


class RoomService:
    def __init__(self, room_repository: RoomRepository | None = None):
        self.room_repository = room_repository or RoomRepository()

    def create_room(self, name: str, description: str | None = None):
        return self.room_repository.create(name, description)

    def list_rooms(self):
        return self.room_repository.list_rooms()

    def get_room(self, room_id: int):
        return self.room_repository.get_by_id(room_id)

    def update_room(self, room_id: int, name: str | None = None, description: str | None = None):
        return self.room_repository.update(room_id, name, description)

    def delete_room(self, room_id: int):
        return self.room_repository.delete(room_id)
