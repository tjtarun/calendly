from flask_restful import reqparse

from app.managers import UserRecurringSlotManager
from app.api.base import BaseResourcesView
from app.api.error import HTTPBadRequest


class UserRecurringSlotResource(BaseResourcesView):
    slot_patch_parser = reqparse.RequestParser()
    slot_patch_parser.add_argument("start_time", type=str, location=["form", "json"])
    slot_patch_parser.add_argument("end_time", type=str, location=["form", "json"])
    slot_patch_parser.add_argument("slot_type", type=str, location=["form", "json"])
    slot_patch_parser.add_argument("day", type=int, location=["form", "json"])

    def patch(self, user_recurring_slot_id):
        kwargs = self.slot_patch_parser.parse_args()
        try:
            user_recurring_slot = UserRecurringSlotManager.update_user_recurring_slot(
                user_recurring_slot_id=user_recurring_slot_id, data=kwargs
            )
        except ValueError as error:
            raise HTTPBadRequest(str(error))
        return user_recurring_slot.serialize()

    def delete(self, user_recurring_slot_id):
        UserRecurringSlotManager.delete_user_recurring_slot(
            user_recurring_slot_id=user_recurring_slot_id
        )
