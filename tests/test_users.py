from app import schemas
from jose import jwt
from app.config import settings
import pytest

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'this is my first api'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello@gmail.com", "password":"hello"})
    new_user = schemas.RespondUser(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login", data={"username": test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("data,status_code",[
    ({"password": "hello"},422),
    ({"username": "hello@gmail.com"},422),
    ({"username": "wemail@gmail.com", "password": "hello"},403),
    ({"username": "hello@gmail.com", "password": "wpwd"},403),
    ({"username": "wemail@gmail.com", "password": "wpwd"},403)
])
def test_invalid_login(client,data,status_code):
    res = client.post("/login", data=data)
    assert res.status_code==status_code

def test_view_user(client,test_user):
    user_id = test_user['id']
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json().get("id") == user_id
    assert res.json().get("email") == test_user["email"]
