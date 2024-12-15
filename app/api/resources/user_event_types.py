from flask_restful import reqparse

from app.api.base import BaseResourcesView
from app.api.error import HTTPBadRequest
from app.managers.user_event_type_manager import UserEventTypeManager


class UserEventTypesResource(BaseResourcesView):

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument("user_id", type=str, location=["form", "json"])
    post_request_parser.add_argument("schedule_id", type=str, location=["form", "json"])
    post_request_parser.add_argument("event_type", type=str, location=["form", "json"])
    post_request_parser.add_argument("code", type=str, location=["form", "json"])

    def post(self):
        kwargs = self.post_request_parser.parse_args()
        try:
            user_event_type = UserEventTypeManager.create_event_type(**kwargs)
        except Exception as error:
            raise HTTPBadRequest(str(error))
        return user_event_type.serialize()
