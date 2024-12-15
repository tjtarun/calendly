from sqlalchemy.exc import IntegrityError

from app import db, app
from app.models import User


class UserManager:
    @staticmethod
    def get_user_by_id(user_id):
        user = User.get_by_id(type_id=user_id)
        return user

    @staticmethod
    def create_user(data):
        try:
            user = User.create(**data)
        except IntegrityError as e:
            db.session.rollback()
            app.logger.info(str(e))
            raise ValueError(str(e))
        return user

    @staticmethod
    def update_user(user_id, data):
        user = User.get_by_id(user_id)
        if not user:
            raise Exception("User not found!")
        user.update(**data)
        return user
