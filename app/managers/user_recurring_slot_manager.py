import datetime

from app.models import UserRecurringSlot
from app.utils.datetime_util import str_time_to_time


class UserRecurringSlotManager:
    @staticmethod
    def create_user_slots(user_id, slots):
        result = []
        for slot in slots:
            # > Retrieve start_time in ISO 8601 format from the request
            slot["start_time"] = str_time_to_time(slot.get("start_time"))
            slot["end_time"] = str_time_to_time(slot.get("end_time"))
            user_recurring_slot = UserRecurringSlot.create(user_id=user_id, **slot)
            result.append(user_recurring_slot.serialize())
        return result

    @staticmethod
    def get_user_recurring_slots(user_id):
        user_slots = UserRecurringSlot.filter_by_user_id(user_id=user_id).all()
        return [user_slot.serialize() for user_slot in user_slots]

    @staticmethod
    def update_user_recurring_slot(user_recurring_slot_id, data):
        user_recurring_slot = UserRecurringSlot.get_by_id(
            type_id=user_recurring_slot_id
        )
        if not user_recurring_slot:
            raise ValueError("Invalid user_recurring_slot_id")

        data["start_time"] = str_time_to_time(data.get("start_time"))
        data["end_time"] = str_time_to_time(data.get("end_time"))
        user_recurring_slot.update(**data)
        return user_recurring_slot

    @staticmethod
    def delete_user_recurring_slot(user_recurring_slot_id):
        UserRecurringSlot.delete(user_recurring_slot_id)
