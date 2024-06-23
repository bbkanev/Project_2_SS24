from app import create_app, db
from . import client, app
from app.models import Test, Question


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Quick Tests" in response.data


def test_register_route(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data


def test_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


def test_add_test_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        response = client.get('/add_test')
        assert response.status_code == 200
        assert b"Add Test" in response.data


def test_edit_test_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        # Create a test and get its ID
        response = client.post('/add_test', data=dict(name="Sample Test", time=10), follow_redirects=True)
        assert response.status_code == 200

        test = db.session.query(Test).filter_by(name="Sample Test").first()
        test_id = test.id

        response = client.get(f'/edit_test/{test_id}')
        assert response.status_code == 200
        assert b"Edit Test" in response.data


def test_add_question_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        client.post('/add_test', data=dict(name="Sample Test", time=10), follow_redirects=True)

        test = db.session.query(Test).filter_by(name="Sample Test").first()
        test_id = test.id

        response = client.get(f'/add_question/{test_id}')
        assert response.status_code == 200
        assert b"Add Question" in response.data


def test_edit_question_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        response = client.post('/add_test', data=dict(name="Sample Test", time=10), follow_redirects=True)

        assert response.status_code == 200

        test = db.session.query(Test).filter_by(name="Sample Test").first()
        test_id = test.id

        response = client.post(f'/add_question/{test_id}', data=dict(question="Sample Question", answer="Answer", option1="Option 1", option2="Option 2", option3="Option 3", points=5), follow_redirects=True)

        assert response.status_code == 200

        question = db.session.query(Question).filter_by(question="Sample Question").first()
        question_id = question.id

        response = client.get(f'/edit_question/{question_id}')
        assert response.status_code == 200
        assert b"Edit Question" in response.data


def test_delete_question_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        client.post('/add_test', data=dict(name="Sample Test", time=10), follow_redirects=True)

        test = db.session.query(Test).filter_by(name="Sample Test").first()
        test_id = test.id

        client.post(f'/add_question/{test_id}', data=dict(question="Sample Question", answer="Answer", option1="Option 1", option2="Option 2", option3="Option 3", points=5), follow_redirects=True)

        question = db.session.query(Question).filter_by(question="Sample Question").first()
        question_id = question.id

        response = client.post(f'/delete_question/{question_id}', follow_redirects=True)
        assert response.status_code == 200


def test_publish_test_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        client.post('/add_test', data=dict(name="Sample Test", time=10), follow_redirects=True)

        test = db.session.query(Test).filter_by(name="Sample Test").first()
        test_id = test.id

        response = client.post(f'/publish_test/{test_id}', follow_redirects=True)
        assert response.status_code == 200
        assert b"Test published successfully" in response.data or b"Test withdraw successfully" in response.data


def test_attempt_test_route(client):
    with client:
        client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
        client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
        client.post('/add_test', data=dict(name="Sample Test", time=10), follow_redirects=True)

        test = db.session.query(Test).filter_by(name="Sample Test").first()
        test_id = test.id

        response = client.get(f'/attempt_test/{test_id}')
        assert response.status_code == 200


def test_logout_route(client):
    client.post('/register', data=dict(username="testuser", email="test@example.com", password="Test!1234", confirm_password="Test!1234"), follow_redirects=True)
    client.post('/login', data=dict(email="test@example.com", password="Test!1234"), follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b"Logged out successfully" in response.data