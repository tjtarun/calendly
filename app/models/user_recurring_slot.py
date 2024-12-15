import datetime

from app import db

from .base import BaseModelMixin, generate_uuid4
from sqlalchemy.dialects.postgresql import UUID


class UserRecurringSlot(BaseModelMixin):
    class SlotType:
        AVAILABLE = "AVAILABLE"
        BUSY = "BUSY"

    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)

    schedule_id = db.Column(
        "schedule_id", UUID(as_uuid=True), nullable=False, index=True
    )
    day = db.Column(db.Integer, nullable=False, default=0)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    recurring_start_date = db.Column(db.DateTime, nullable=False)
    recurring_end_date = db.Column(db.DateTime, nullable=False)

    slot_type = db.Column(
        "slot_type",
        db.String(25),
        nullable=False,
    )

    @classmethod
    def create(cls, **kwargs):
        recurring_start_date = datetime.datetime(2024, 1, 1, 0, 0)
        recurring_end_date = datetime.datetime(2026, 1, 1, 0, 0)
        user_slot = UserRecurringSlot(
            id=kwargs.get("id") or generate_uuid4(),
            user_id=kwargs.get("user_id"),
            slot_type=kwargs.get("slot_type") or cls.SlotType.AVAILABLE,
            day=kwargs.get("day"),
            start_time=kwargs.get("start_time"),
            end_time=kwargs.get("end_time"),
            recurring_start_date=recurring_start_date,
            recurring_end_date=recurring_end_date,
            schedule_id=kwargs.get("schedule_id"),
        )

        db.session.add(user_slot)
        db.session.commit()
        return user_slot

    def update(self, **kwargs):
        args = [
            "start_time",
            "end_time",
            "slot_type",
            "day",
            "recurring_start_date",
            "recurring_end_date",
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
            "day": self.day,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "slot_type": self.slot_type,
            "id": str(self.id),
            "user_id": str(self.user_id),
            "schedule_id": str(self.schedule_id),
            "recurring_start_date": str(self.recurring_start_date),
            "recurring_end_date": str(self.recurring_end_date),
        }

    @classmethod
    def filter_by_user_id(cls, user_id):
        return cls.query.filter(cls.user_id == user_id)
