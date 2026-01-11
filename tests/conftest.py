from fastapi.testclient import TestClient
from app.main1 import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db,Base
import pytest
from app.oauth2 import create_accesstoken
from app import models

sqlalchemy_db_url=f"postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"
engine=create_engine(sqlalchemy_db_url)
session_local=sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=session_local()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data={"email": "hello@gmail.com",
               "password": "hello"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user=res.json()
    new_user["password"]=user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data={"email": "me@gmail.com",
               "password": "me"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user=res.json()
    new_user["password"]=user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_accesstoken({"user_id":test_user['id']})

@pytest.fixture
def auth_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(session,test_user,test_user2):
    post_data=[{"title": "hello", "content":"i am saying hello", "post": False,"rating": 7, "user_id": test_user['id']},
               {"title": "me", "content":"hi its me", "post": True,"rating": 9, "user_id": test_user2['id']}]
    def create_posts_model(post):
        return models.Post(**post) 
    post_map = map(create_posts_model, post_data)
    posts=list(post_map)
    session.add_all(posts)
    session.commit()
    final = session.query(models.Post).all()
    return final