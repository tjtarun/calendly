from flask_restful import reqparse

from app.managers import UserSlotManager
from app.api.base import BaseResourcesView


class UserSlotsResource(BaseResourcesView):
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument("user_id", type=str)
    get_request_parser.add_argument("start_datetime", type=int)
    get_request_parser.add_argument("end_datetime", type=int)

    def get(self):
        kwargs = self.get_request_parser.parse_args()
        start_datetime = kwargs.get("start_datetime")
        end_datetime = kwargs.get("end_datetime")
        user_id = kwargs.get("user_id")

        user_slots = UserSlotManager.get_user_slots_for_range(
            user_id=user_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        return dict(user_slots=user_slots)

    post_request_parser = reqparse.RequestParser()

    post_request_parser.add_argument(
        "user_id", type=str, location=["form", "json"], required=True
    )
    post_request_parser.add_argument(
        "user_slots", type=dict, action="append", location=["form", "json"]
    )

    user_slot_post_parser = reqparse.RequestParser()
    user_slot_post_parser.add_argument(
        "start_datetime", type=int, location=["form", "json"]
    )
    user_slot_post_parser.add_argument(
        "end_datetime", type=int, location=["form", "json"]
    )
    user_slot_post_parser.add_argument("slot_type", type=int, location=["form", "json"])

    def post(self):
        kwargs = self.post_request_parser.parse_args()
        user_id = kwargs.get("user_id")
        user_slots = UserSlotManager.create_user_slots(
            user_id=user_id,
            user_slots=kwargs.get("user_slots"),
        )
        return dict(user_slots=user_slots)
