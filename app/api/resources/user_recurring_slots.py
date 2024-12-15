from flask_restful import reqparse
from flask_restful.inputs import boolean
from flask import request
from app.managers import UserRecurringSlotManager, UserSlotManager
from app.api.base import BaseResourcesView


class UserRecurringSlotsResource(BaseResourcesView):
    """
    View Calendar Week API.
    """

    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument("with_date_slots", type=boolean, location="args")
    get_request_parser.add_argument("user_id", type=str, location="args")
    get_request_parser.add_argument("start_datetime", type=int, location="args")
    get_request_parser.add_argument("end_datetime", type=int, location="args")

    def get(self):
        kwargs = self.get_request_parser.parse_args()
        with_date_slots = kwargs.get("with_date_slots")
        start_datetime = kwargs.get("start_datetime")
        end_datetime = kwargs.get("end_datetime")
        user_id = kwargs.get("user_id")

        user_recurring_slots = UserRecurringSlotManager.get_user_recurring_slots(
            user_id=user_id
        )

        if not with_date_slots:
            return dict(
                user_recurring_slots=user_recurring_slots,
            )

        user_slots = []
        if start_datetime and end_datetime:
            user_slots = UserSlotManager.get_user_slots_for_range(
                user_id=user_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )

        return dict(user_recurring_slots=user_recurring_slots, user_slots=user_slots)

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument("user_id", type=str, location=["form", "json"])
    post_request_parser.add_argument(
        "slots", type=dict, action="append", location=["form", "json"]
    )

    slot_post_parser = reqparse.RequestParser()
    slot_post_parser.add_argument("schedule_id", type=str, location=["form", "json"])
    slot_post_parser.add_argument("start_time", type=str, location=["form", "json"])
    slot_post_parser.add_argument("end_time", type=str, location=["form", "json"])
    slot_post_parser.add_argument("slot_type", type=str, location=["form", "json"])
    slot_post_parser.add_argument("day", type=int, location=["form", "json"])

    def post(self):
        kwargs = self.post_request_parser.parse_args()
        user_id = kwargs.get("user_id")
        user_recurring_slots = UserRecurringSlotManager.create_user_slots(
            user_id=user_id, slots=kwargs.get("slots")
        )
        return dict(user_recurring_slots=user_recurring_slots)
