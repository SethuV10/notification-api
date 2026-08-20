import datetime

from repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, message_repository: MessageRepository | None = None):
        self.message_repository = message_repository or MessageRepository()

    def create_message(self, payload: dict):
        payload = dict(payload)
        payload["expires_at"] = (datetime.datetime.now() + datetime.timedelta(minutes=60)).isoformat()
        return self.message_repository.create(payload)

    def list_active_messages(self, room_id: int):
        if room_id == 1000:
            # Special case: fetch all active messages
            return self.message_repository.get_all_Active_messages()
        else:
            # Normal case: fetch only messages for the given room
            return self.message_repository.get_active_by_room(room_id)


    
    def list_active_messages_by_team(self, team_id: int):
        return self.message_repository.get_active_by_team(team_id)
    
    def list_active_messages_by_staff(self, staff_id: int):
        return self.message_repository.get_active_by_staff(staff_id)

    def list_history(self):
        return self.message_repository.get_history()

    def acknowledge_message(self, message_id: int):
        now = datetime.datetime.now().isoformat()
        return self.message_repository.acknowledge(message_id, now)
