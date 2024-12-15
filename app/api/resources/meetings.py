from flask_restful import reqparse

from app.api.error import HTTPBadRequest
from app.managers import UserSlotManager
from app.api.base import BaseResourcesView
from app.models import UserSlot


class MeetingsResource(BaseResourcesView):
    post_request_parser = reqparse.RequestParser()

    post_request_parser.add_argument(
        "request_user_id", type=str, location=["form", "json"], required=True
    )
    post_request_parser.add_argument(
        "user_event_type_id", type=str, location=["form", "json"]
    )
    post_request_parser.add_argument("user_slot", type=dict, location=["form", "json"])

    user_slot_post_parser = reqparse.RequestParser()
    user_slot_post_parser.add_argument(
        "start_datetime", type=int, location=["form", "json"]
    )
    user_slot_post_parser.add_argument(
        "end_datetime", type=int, location=["form", "json"]
    )
    user_slot_post_parser.add_argument("duration", type=int, location=["form", "json"])
    user_slot_post_parser.add_argument(
        "slot_type",
        default=UserSlot.SlotType.MEETING,
        type=str,
        location=["form", "json"],
    )

    def post(self):
        kwargs = self.post_request_parser.parse_args()
        request_user_id = kwargs.get("request_user_id")
        user_event_type_id = kwargs.get("user_event_type_id")
        try:
            user_slot = UserSlotManager.execute_book_meeting(
                request_user_id=request_user_id,
                user_event_type_id=user_event_type_id,
                user_slot=kwargs.get("user_slot"),
            )
        except ValueError as e:
            raise HTTPBadRequest(str(e))
        return dict(user_slot=user_slot)
