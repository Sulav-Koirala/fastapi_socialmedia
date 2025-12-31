from app import schemas
from .db import client

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'this is my first api'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello@gmail.com", "password":"hello"})
    new_user = schemas.RespondUser(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/login", data={"username": "hello@gmail.com", "password":"hello"})
    assert res.status_code == 200