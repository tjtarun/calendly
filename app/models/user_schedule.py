from app import db

from .base import BaseModelMixin, generate_uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index


class UserSchedule(BaseModelMixin):
    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)
    schedule_name = db.Column(db.String(50), nullable=False)
    schedule_code = db.Column(db.String(50), unique=True)

    __table_args__ = (
        Index(
            "ix_user_schedule_user_id_code",
            "user_id",
            "schedule_code",
            unique=True,
        ),
    )

    @classmethod
    def create(cls, **kwargs):
        user_schedule = UserSchedule(
            id=kwargs.get("id") or generate_uuid4(),
            user_id=kwargs.get("user_id"),
            schedule_name=kwargs.get("schedule_name"),
            schedule_code=kwargs.get("schedule_code"),
        )

        db.session.add(user_schedule)
        db.session.commit()
        return user_schedule

    def update(self, **kwargs):
        args = [
            "schedule_name",
            "schedule_code",
        ]

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
            "user_id": str(self.user_id),
            "schedule_name": self.schedule_name,
            "schedule_code": self.schedule_code,
        }
