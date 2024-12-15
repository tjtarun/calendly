import datetime
import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID

from app import db


def generate_uuid4():
    return uuid.uuid4()


class BaseModelMixin(db.Model):
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        primary_key=True,
        default=uuid.uuid4,
    )
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_on = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )
    meta_data = db.Column("meta", JSON, default=dict)

    @property
    def created_on_ts(self):
        return self.created_on.timestamp()

    @property
    def updated_on_ts(self):
        return self.updated_on.timestamp()

    def serialize(self):
        return {
            "id": str(self.id),
            "created_on_ts": self.created_on_ts,
            "updated_on_ts": self.updated_on_ts,
        }

    @classmethod
    def get_by_ids(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).all()

    @classmethod
    def get_by_id(cls, type_id):
        return cls.query.filter(cls.id == type_id).first()

    @classmethod
    def bulk_serialize(cls, entities, ids=False):
        return (
            [str(entity.id) for entity in entities if entity]
            if ids
            else [entity.serialize() for entity in entities if entity]
        )

    @classmethod
    def delete(cls, _id):
        print("deleting: ", str(_id))
        obj = cls.get_by_id(_id)
        print(obj)
        db.session.delete(obj)
        db.session.commit()
