from flask_restful import reqparse

from app.managers import UserManager
from app.api.base import BaseResourcesView
from app.api.error import HTTPBadRequest


class UsersResource(BaseResourcesView):

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument("first_name", type=str, location=["form", "json"])
    post_request_parser.add_argument("last_name", type=str, location=["form", "json"])
    post_request_parser.add_argument("username", type=str, location=["form", "json"])

    def post(self):
        kwargs = self.post_request_parser.parse_args()
        user_manager = UserManager()
        try:
            user = user_manager.create_user(kwargs)
        except ValueError as error:
            raise HTTPBadRequest(str(error))
        return user.serialize()
