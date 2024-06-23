# tests/test_models.py

import pytest
from app import create_app, db
from app.models import User, Test, Question, Attempt
import uuid
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
