from app import db

from .base import BaseModelMixin, generate_uuid4


class User(BaseModelMixin):
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), default="")

    @property
    def full_name(self):
        return (
            (self.first_name + " " + self.last_name)
            if self.last_name
            else self.first_name
        )

    @classmethod
    def create(cls, **kwargs):
        user = User(
            id=kwargs.get("user_id") or generate_uuid4(),
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name", ""),
            username=kwargs.get("username"),
        )

        db.session.add(user)
        db.session.commit()
        return user

    def update(self, **kwargs):
        args = ["first_name", "last_name", "username", "password"]

        prev_data = {}

        for x in args:
            if kwargs.get(x) is not None:
                prev_data[x] = getattr(self, x)
                value = kwargs.get(x)
                setattr(self, x, value)

        db.session.add(self)
        db.session.commit()

    def serialize(self, **kwargs):
        return {
            "id": str(self.id),
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name if self.last_name else "",
            "name": self.full_name,
        }
