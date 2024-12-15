from app.models import UserSchedule


class UserScheduleManager:
    @staticmethod
    def create_user_schedule(data):
        user_schedule = UserSchedule.create(**data)
        return user_schedule
