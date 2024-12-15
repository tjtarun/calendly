from app import db

from .base import BaseModelMixin, generate_uuid4
from sqlalchemy.dialects.postgresql import UUID


class UserSlotGuest(BaseModelMixin):
    guest_user_id = db.Column(
        "guest_user_id", UUID(as_uuid=True), nullable=False, index=True
    )
    guest_user_role = db.Column(
        "guest_user_role",
        db.String(25),
        nullable=False,
    )

    # state = accepted/rejected/maybe rsvp
    # guest user role can have its own setting - host, co-host, active participants, passive participants.
    # if we choose to host our own audio video or if we integrate with zoom, google meet - we pass on the information

    user_slot_id = db.Column(
        "user_slot_id", UUID(as_uuid=True), nullable=False, index=True
    )

    @classmethod
    def create(cls, **kwargs):
        meeting_guest = cls(
            id=kwargs.get("id") or generate_uuid4(),
            user_slot_id=kwargs.get("user_slot_id"),
            guest_user_id=kwargs.get("guest_user_id"),
            guest_user_role=kwargs.get("guest_user_role"),
        )

        db.session.add(meeting_guest)
        db.session.commit()
        return meeting_guest

    def update(self, **kwargs):
        args = [
            "guest_user_role",
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
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "slot_type": self.slot_type,
            "user_id": str(self.user_id),
        }
