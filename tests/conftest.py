from fastapi.testclient import TestClient
from app.main1 import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db,Base
import pytest

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

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
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