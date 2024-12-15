from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import flag_modified

from app import db

from .base import BaseModelMixin, generate_uuid4
from ..utils.datetime_util import timestamp_to_datetime


class UserSlot(BaseModelMixin):
    class SlotType:
        AVAILABLE = "AVAILABLE"
        BUSY = "BUSY"
        MEETING = "MEETING"

    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)
    booked_by_user_id = db.Column(
        "booked_by_user_id", UUID(as_uuid=True), nullable=True, index=True
    )

    user_event_type_id = db.Column(
        "user_event_type_id", UUID(as_uuid=True), nullable=True, index=True
    )
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    slot_type = db.Column(
        "slot_type",
        db.String(25),
        nullable=False,
    )

    @classmethod
    def create(cls, **kwargs):
        user_slot = cls(
            id=kwargs.get("id") or generate_uuid4(),
            user_id=kwargs.get("user_id"),
            user_event_type_id=kwargs.get("user_event_type_id"),
            slot_type=kwargs.get("slot_type") or cls.SlotType.MEETING,
            start_datetime=timestamp_to_datetime(kwargs.get("start_datetime")),
            end_datetime=timestamp_to_datetime(kwargs.get("end_datetime")),
        )

        db.session.add(user_slot)
        db.session.commit()
        return user_slot

    def update(self, **kwargs):
        args = [
            "start_datetime",
            "end_datetime",
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
            "start_datetime": str(self.start_datetime),
            "end_datetime": str(self.end_datetime),
            "slot_type": self.slot_type,
            "user_id": str(self.user_id),
            "id": str(self.id),
        }

    @classmethod
    def filter_by_user_id_in_range(cls, user_id, start_datetime, end_datetime):
        return cls.query.filter(
            cls.user_id == user_id,
            cls.start_datetime < timestamp_to_datetime(end_datetime),
            cls.end_datetime > timestamp_to_datetime(start_datetime),
        ).all()

    @property
    def schedule_id(self):
        """
        When adding date specific availability. We need to provide for which schedule the availability is on.
        """
        return self.meta_data.get("schedule_id")

    @schedule_id.setter
    def schedule_id(self, value):
        if not self.meta_data:
            self.meta_data = dict()
        self.meta_data["schedule_id"] = value
        flag_modified(self, "schedule_id")
