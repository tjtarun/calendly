from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index

from app import db

from .base import BaseModelMixin, generate_uuid4


class UserEventType(BaseModelMixin):
    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)
    schedule_id = db.Column(
        "schedule_id", UUID(as_uuid=True), nullable=True, index=True
    )
    event_type = db.Column(db.String(50), nullable=False)
    code = db.Column(
        db.String(50), nullable=False
    )  # short_code / unique user event url for booking this event with the user.
    is_deleted = db.Column("is_deleted", db.Boolean, default=False, nullable=False)

    __table_args__ = (
        Index(
            "ix_user_event_type_user_id_code",
            "user_id",
            "code",
            unique=True,
        ),
    )

    @classmethod
    def create(cls, **kwargs):
        user_event_type = UserEventType(
            id=kwargs.get("id") or generate_uuid4(),
            code=kwargs.get("code"),
            user_id=kwargs.get("user_id"),
            event_type=kwargs.get("event_type"),
            schedule_id=kwargs.get("schedule_id"),
        )

        db.session.add(user_event_type)
        db.session.commit()
        return user_event_type

    def update(self, **kwargs):
        args = [
            "event_type",
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
            "event_type": self.event_type,
            "is_deleted": self.is_deleted,
            "buffer_settings": self.buffer_settings,
            "available_durations": self.available_durations,
        }

    @property
    def buffer_settings(self):
        """

        :return: {
            "upper_buffer":
            "lower_buffer":
        }
        """
        return self.meta_data.get("buffer_settings") or {
            "upper_buffer": 0,
            "lower_buffer": 0,
        }

    @buffer_settings.setter
    def buffer_settings(self, value):
        if not self.meta_data:
            self.meta_data = dict()
        self.meta_data["buffer_settings"] = value
        flag_modified(self, "meta_data")

    @property
    def upper_buffer(self):
        return self.buffer_settings.get("upper_buffer", 0)

    @property
    def lower_buffer(self):
        return self.buffer_settings.get("lower_buffer", 0)

    @property
    def available_durations(self):
        """
        for future use cases where 1 event type can have multiple durations available.
        event type can have pricing related to it
        """
        return self.meta_data.get("available_durations") or [
            {
                "name": "Full slot",
                "default": True,
                "duration": 30,
                "pricing": {"amount": 300, "currency": "INR"},
            },
            {"name": "Half slot", "duration": 15},
        ]

    @available_durations.setter
    def available_durations(self, value):
        if not self.meta_data:
            self.meta_data = dict()
        self.meta_data["available_durations"] = value
        flag_modified(self, "meta_data")
