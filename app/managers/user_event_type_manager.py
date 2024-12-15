from app.models import UserEventType


class UserEventTypeManager:
    @staticmethod
    def create_event_type(data):
        user_event_type = UserEventType.create(**data)
        return user_event_type
