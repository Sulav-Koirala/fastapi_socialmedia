from fastapi.testclient import TestClient
from app.main1 import app
from app import schemas
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db,Base

sqlalchemy_db_url=f"postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"
engine=create_engine(sqlalchemy_db_url)
session_local=sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db]=override_get_db

Base.metadata.create_all(bind=engine)

client=TestClient(app)

def test_root():
    res = client.get("/")
    assert res.json().get('message') == 'this is my first api'
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"email": "hello@gmail.com", "password":"hello"})
    new_user = schemas.RespondUser(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
