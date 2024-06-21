import uuid
from sqlalchemy.dialects.postgresql import UUID
from . import db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(150), unique=False, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'