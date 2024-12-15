import datetime

from app.models import UserSlot, UserSlotGuest, UserEventType, UserRecurringSlot
from app.models.user_schedule import UserSchedule


class UserSlotManager:
    @staticmethod
    def create_user_slots(user_id, user_slots):
        result = []
        for slot in user_slots:
            user_slot = UserSlot.create(user_id=user_id, **slot)
            result.append(user_slot.serialize())
        return result

    @staticmethod
    def get_user_slots_for_range(user_id, start_datetime, end_datetime):
        user_slots = UserSlot.filter_by_user_id_in_range(
            user_id=user_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        return [user_slot.serialize() for user_slot in user_slots]

    @staticmethod
    def delete_user_slot(user_slot_id):
        UserSlot.delete(user_slot_id)

    @classmethod
    def execute_action(cls, user_slot_id, action, action_data):
        return getattr(cls, "execute_" + action)(user_slot_id, action_data)

    @classmethod
    def execute_book_meeting(cls, request_user_id, user_slot, user_event_type_id):
        user_event_type = UserEventType.get_by_id(user_event_type_id)
        if not user_event_type:
            return False, "Invalid event type"
        host_user_id = str(user_event_type.user_id)
        schedule_id = user_event_type.schedule_id
        schedule = UserSchedule.get_by_id(schedule_id)
        if not schedule:
            return False, "Schedule not found for the given event type"

        try:
            can_book = cls._can_book_meeting(
                request_user_id, host_user_id, user_slot, user_event_type, schedule
            )
        except ValueError as e:
            return False, str(e)

        user_slots = cls.create_user_slots(host_user_id, user_slots=[user_slot])
        cls.execute_add_guest(
            user_slot_id=str(user_slots[0]["id"]),
            guest_user_id=host_user_id,
            guest_user_role="HOST",
        )
        cls.execute_add_guest(
            user_slot_id=str(user_slots[0]["id"]),
            guest_user_id=request_user_id,
            guest_user_role="GUEST",
        )

    @staticmethod
    def check_if_user_is_busy(user_id, start_datetime, end_datetime):
        user_slots = UserSlot.filter_by_user_id_in_range(
            user_id=user_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        any_busy_slot = any(
            user_slot.slot_type in [UserSlot.SlotType.BUSY, UserSlot.SlotType.MEETING]
            for user_slot in user_slots
        )
        if any_busy_slot:
            return True, user_slots
        return False, user_slots

    @staticmethod
    def check_available_recurring_user_slot(
        user_id, start_datetime_obj, end_datetime_obj
    ):
        meeting_date = start_datetime_obj.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        meeting_time_start = start_datetime_obj.time()
        meeting_time_end = end_datetime_obj.time()

        # > Get the day index (0=Monday, 6=Sunday)
        meeting_day = start_datetime_obj.weekday()

        host_recurring_available_slots = UserRecurringSlot.query.filter(
            UserRecurringSlot.user_id == user_id,
            UserRecurringSlot.slot_type == UserRecurringSlot.SlotType.AVAILABLE,
            UserRecurringSlot.day == str(meeting_day),
            UserRecurringSlot.recurring_start_date < meeting_date,
            UserRecurringSlot.recurring_end_date > meeting_date,
            UserRecurringSlot.start_time <= meeting_time_start,
            UserRecurringSlot.end_time >= meeting_time_end,
        ).all()

        # print(
        #     user_id,
        #     UserRecurringSlot.SlotType.AVAILABLE,
        #     meeting_date,
        #     str(meeting_day),
        #     meeting_time_start,
        #     meeting_time_end,
        # )
        if host_recurring_available_slots:
            return True
        return False

    @classmethod
    def _can_book_meeting(
        cls, request_user_id, host_user_id, user_slot, user_event_type, schedule
    ):
        schedule_id = str(schedule.id)

        start_datetime = user_slot["start_datetime"]
        duration = user_slot["duration"]
        start_datetime_obj = datetime.datetime.fromtimestamp(start_datetime)
        end_datetime_obj = start_datetime_obj + datetime.timedelta(minutes=duration)
        #
        # # > todo check if requesting user is busy with other meeting
        # can not support this check for now. as we are not creating user slot for requesting user.
        # any_busy_slot_of_requesting_user, _ = cls.check_if_user_is_busy(
        #     user_id=request_user_id,
        #     start_datetime=start_datetime_obj.timestamp(),
        #     end_datetime=end_datetime_obj.timestamp(),
        # )
        # if any_busy_slot_of_requesting_user:
        #     raise ValueError("Conflict Found. You have existing user slot")

        # > check if host user is busy with other meeting
        slot_to_be_booked_start = start_datetime_obj - datetime.timedelta(
            minutes=user_event_type.upper_buffer
        )
        slot_to_be_booked_end = end_datetime_obj + datetime.timedelta(
            minutes=user_event_type.upper_buffer
        )
        any_busy_slot_of_host_user, host_user_all_slots = cls.check_if_user_is_busy(
            user_id=host_user_id,
            start_datetime=slot_to_be_booked_start.timestamp(),
            end_datetime=slot_to_be_booked_end.timestamp(),
        )
        if any_busy_slot_of_host_user:
            raise ValueError(
                "Conflict Found. Host have existing meeting in given slot."
            )

        # > check if any date specific availability has been added by user for the given schedule.
        host_date_specific_available_slots = any(
            user_slot.slot_type in [UserSlot.SlotType.AVAILABLE]
            and user_slot.schedule_id == schedule_id
            for user_slot in host_user_all_slots
        )
        if host_date_specific_available_slots:
            return True

        # > check if any recurring availability - any slot has been added by user for the given schedule.
        # > that is superset of the requested meeting time
        if cls.check_available_recurring_user_slot(
            host_user_id, slot_to_be_booked_start, slot_to_be_booked_end
        ):
            return True

        raise ValueError("Host is not available, But also do not have conflicts.")

    @staticmethod
    def execute_add_guest(user_slot_id, guest_user_id, guest_user_role):
        return UserSlotGuest.create(
            user_slot_id=user_slot_id,
            guest_user_id=guest_user_id,
            guest_user_role=guest_user_role,
        )
