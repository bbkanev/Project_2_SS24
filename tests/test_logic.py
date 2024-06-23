# tests/test_logic.py

import pytest
from app.logic import Logic
from app.models import User, Test, Question, Attempt
from . import client, app
from app import create_app, db
from datetime import datetime
import uuid


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


def test_validate_password():
    valid, message = Logic.validate_password('Testpassword1!')
    assert valid is True

    valid, message = Logic.validate_password('short')
    assert valid is False
    assert message == "Password must be at least 8 characters long"


def test_validate_email():
    valid, message = Logic.validate_email('test@example.com')
    assert valid is True

    valid, message = Logic.validate_email('invalid-email')
    assert valid is False
    assert message == "Invalid email address"


def test_add_new_test(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        user = User.query.filter_by(email='testuser@example.com').first()
        success, message = Logic.add_new_test('Sample Test', 30, False, user.id)
        assert success
        assert message == 'Test added successfully'

        test = Test.query.filter_by(name='Sample Test').first()
        assert test is not None
        assert test.time == 30
        assert test.created_by == user.id


def test_add_new_question(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        user = User.query.filter_by(email='testuser@example.com').first()
        test = Test(name='Sample Test', time=30, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        success, message = Logic.add_new_question('Sample Question', 'Answer', 'Option1', 'Option2', 'Option3', 10,
                                                  test.id)
        assert success
        assert message == 'Question added successfully'

        question = Question.query.filter_by(question='Sample Question').first()
        assert question is not None
        assert question.answer == 'Answer'
        assert question.test_id == test.id


def test_get_user_by_id(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        user = User.query.filter_by(email='testuser@example.com').first()
        retrieved_user = Logic.get_user_by_id(user.id)
        assert retrieved_user is not None
        assert retrieved_user.email == 'testuser@example.com'


def test_calculate_total_score(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        user = User.query.filter_by(email='testuser@example.com').first()
        test = Test(name='Sample Test', time=30, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        Logic.add_new_question('Sample Question 1', 'Answer', 'Option1', 'Option2', 'Option3', 10, test.id)
        Logic.add_new_question('Sample Question 2', 'Answer', 'Option1', 'Option2', 'Option3', 20, test.id)

        total_score = Logic.calculate_total_score(test.id)
        assert total_score == 30


def test_delete_question(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        user = User.query.filter_by(email='testuser@example.com').first()
        test = Test(name='Sample Test', time=30, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        Logic.add_new_question('Sample Question', 'Answer', 'Option1', 'Option2', 'Option3', 10, test.id)
        question = Question.query.filter_by(question='Sample Question').first()

        success, message, test_id = Logic.delete_question(question.id)
        assert success
        assert message == 'Question deleted successfully'
        assert test_id == test.id

        deleted_question = Question.query.get(question.id)
        assert deleted_question is None


def test_shuffle_options(app):
    with app.app_context():
        question = Question(question='Sample Question', answer='Answer', option1='Option1', option2='Option2', option3='Option3', points=10, test_id=uuid.uuid4())
        shuffled_options = Logic.shuffle_options(question)
        assert 'Answer' in shuffled_options
        assert 'Option1' in shuffled_options
        assert 'Option2' in shuffled_options
        assert 'Option3' in shuffled_options


def test_save_attempt(app):
    with app.app_context():
        Logic.add_new_user('testuser', 'Test!1234', 'testuser@example.com', 'Test!1234')
        user = User.query.filter_by(email='testuser@example.com').first()
        test = Test(name='Sample Test', time=30, is_published=False, created_by=user.id)
        db.session.add(test)
        db.session.commit()

        finish_time = datetime.utcnow()
        time_taken = 1200  # 20 minutes
        score = 25
        max_score = 30

        success, message = Logic.save_attempt(test.id, user.id, finish_time, time_taken, score, max_score)
        assert success
        assert message == f"Test submitted successfully! Your score is {score}/{max_score}', 'success'"

        attempt = Attempt.query.filter_by(test_id=test.id, user_id=user.id).first()
        assert attempt is not None
        assert attempt.score == score
        assert attempt.time_taken == time_taken


def test_calculate_time_taken():
    start_time_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    finish_time, time_taken = Logic.calculate_time_taken(start_time_str)
    assert time_taken is not None
    assert finish_time > datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')


def test_get_leaderboard(app):
    with app.app_context():
        user1 = User(username='user1', email='user1@example.com', password='password1')
        user2 = User(username='user2', email='user2@example.com', password='password2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        test = Test(name='Sample Test', time=30, is_published=False, created_by=user1.id)
        db.session.add(test)
        db.session.commit()

        attempt1 = Attempt(test_id=test.id, user_id=user1.id, finish_time=datetime.utcnow(), time_taken=1200, score=25)
        attempt2 = Attempt(test_id=test.id, user_id=user2.id, finish_time=datetime.utcnow(), time_taken=1300, score=28)
        attempt3 = Attempt(test_id=test.id, user_id=user1.id, finish_time=datetime.utcnow(), time_taken=1100, score=25)
        db.session.add_all([attempt1, attempt2, attempt3])
        db.session.commit()

        attempts = Attempt.query.filter_by(test_id=test.id).order_by(Attempt.score.desc(), Attempt.time_taken).all()
        results = Logic.get_leaderboard(attempts)

        assert len(results) == 2  # Only the best attempt for each user
        assert results[0].user_id == user2.id
        assert results[1].user_id == user1.id
        assert results[1].time_taken == 1100  # The better time for user1

