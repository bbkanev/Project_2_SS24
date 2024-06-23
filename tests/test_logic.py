# tests/test_logic.py

import pytest
from app.logic import Logic
from app.models import User, Test, Question, Attempt
from . import client, app


def test_add_new_user(app):
    with app.app_context():
        success, message = Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        assert success
        assert message == 'User registered successfully'

        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'testuser@example.com'


def test_verify_user(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        success, user = Logic.verify_user('testuser@example.com', 'Test!1234')
        assert success
        assert user.username == 'testuser'
        assert user.email == 'testuser@example.com'
