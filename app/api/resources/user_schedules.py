from flask_restful import reqparse

from app.api.base import BaseResourcesView
from app.api.error import HTTPBadRequest
from app.managers.user_schedule_manager import UserScheduleManager


class UserSchedulesResource(BaseResourcesView):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument("user_id", type=str, location=["form", "json"])
    post_request_parser.add_argument(
        "schedule_name", type=str, location=["form", "json"]
    )
    post_request_parser.add_argument(
        "schedule_code", type=str, location=["form", "json"]
    )

    def post(self):
        kwargs = self.post_request_parser.parse_args()
        try:
            user_schedule = UserScheduleManager.create_user_schedule(**kwargs)
        except Exception as error:
            raise HTTPBadRequest(str(error))
        return user_schedule.serialize()
