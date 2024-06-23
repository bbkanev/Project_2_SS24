import uuid
from sqlalchemy.dialects.postgresql import UUID
from . import db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(150), unique=False, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    tests = db.relationship('Test', back_populates='user')
    attempts = db.relationship('Attempt', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Test(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='tests')
    questions = db.relationship('Question', back_populates='test')
    attempts = db.relationship('Attempt', back_populates='test')


class Question(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    points = db.Column(db.Integer, nullable=False)
    test_id = db.Column(UUID(as_uuid=True), db.ForeignKey('test.id'), nullable=False)
    test = db.relationship('Test', back_populates='questions')


class Attempt(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_id = db.Column(UUID(as_uuid=True), db.ForeignKey('test.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    finish_time = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    test = db.relationship('Test', back_populates='attempts')
    user = db.relationship('User', back_populates='attempts')