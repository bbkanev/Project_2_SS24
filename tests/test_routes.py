import pytest
from app import create_app, db
from . import client, app


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Quick Tests" in response.data


def test_register_route(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data
