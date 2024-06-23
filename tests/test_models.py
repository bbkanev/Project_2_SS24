# tests/test_models.py

import pytest
from app import create_app, db
from app.models import User, Test, Question, Attempt
from datetime import datetime
from . import client, app


def test_create_user(app):
    with app.app_context():
        user = User(username='test_user', password='password', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'test_user'
        assert user.email == 'testuser@example.com'


def test_create_test(app):
    with app.app_context():
        user = User(username='test_user', password='password', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        test = Test(name='Sample Test', time=30, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        assert test.id is not None
        assert test.name == 'Sample Test'
        assert test.time == 30


def test_question_model(app):
    with app.app_context():
        user = User(username='testuser', password='Test!1234', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        test = Test(name='Sample Test', time=10, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        question = Question(question='Sample Question', answer='Answer', option1='Option1', option2='Option2',
                            option3='Option3', points=5, test_id=test.id)
        db.session.add(question)
        db.session.commit()

        fetched_question = Question.query.filter_by(question='Sample Question').first()
        assert fetched_question is not None
        assert fetched_question.answer == 'Answer'
        assert fetched_question.points == 5
        assert fetched_question.test_id == test.id


def test_attempt_model(app):
    with app.app_context():
        user = User(username='testuser', password='Test!1234', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        test = Test(name='Sample Test', time=10, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        attempt = Attempt(test_id=test.id, user_id=user.id, finish_time=datetime.utcnow(), time_taken=60.0, score=50)
        db.session.add(attempt)
        db.session.commit()

        fetched_attempt = Attempt.query.filter_by(test_id=test.id).first()
        assert fetched_attempt is not None
        assert fetched_attempt.user_id == user.id
        assert fetched_attempt.score == 50