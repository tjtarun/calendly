from flask_restful import reqparse

from app.managers import UserSlotManager
from app.api.base import BaseResourcesView
from app.api.error import HTTPBadRequest


class UserSlotResource(BaseResourcesView):
    patch_request_parser = reqparse.RequestParser()
    patch_request_parser.add_argument("action", type=str, location=["form", "json"])

    patch_request_parser.add_argument(
        "action_data", type=dict, location=["form", "json"]
    )

    slot_patch_parser = reqparse.RequestParser()
    slot_patch_parser.add_argument("schedule_id", type=str, location=["form", "json"])
    slot_patch_parser.add_argument("start_time", type=int, location=["form", "json"])
    slot_patch_parser.add_argument("end_time", type=int, location=["form", "json"])
    slot_patch_parser.add_argument("slot_type", type=int, location=["form", "json"])
    slot_patch_parser.add_argument("day", type=int, location=["form", "json"])

    def patch(self, user_slot_id):
        kwargs = self.patch_request_parser.parse_args()
        try:
            user_date_slot = UserSlotManager.execute_action(
                user_slot_id=user_slot_id,
                action_data=kwargs.get("action_data"),
                action=kwargs.get("action"),
            )
        except ValueError as error:
            raise HTTPBadRequest(str(error))
        return user_date_slot.serialize()

    def delete(self, user_slot_id):
        UserSlotManager.delete_user_slot(user_slot_id=user_slot_id)
