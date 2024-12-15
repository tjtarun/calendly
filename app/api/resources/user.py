from flask_restful import reqparse

from app.managers import UserManager
from app.api.base import BaseResourcesView
from app.api.error import HTTPNotFound, HTTPBadRequest


class UserResource(BaseResourcesView):
    patch_request_parser = reqparse.RequestParser()
    patch_request_parser.add_argument('first_name', type=str, location=['form', 'json'])
    patch_request_parser.add_argument('last_name', type=str, location=['form', 'json'])
    patch_request_parser.add_argument('username', type=str, location=['form', 'json'])

    def get(self, user_id):
        user = UserManager.get_user_by_id(user_id)
        if not user:
            raise HTTPNotFound('User not found')
        return user.serialize()

    def patch(self, user_id):
        kwargs = self.patch_request_parser.parse_args()
        try:
            user = UserManager.update_user(user_id=user_id, data=kwargs)
        except ValueError as error:
            raise HTTPBadRequest(str(error))
        return user.serialize()
