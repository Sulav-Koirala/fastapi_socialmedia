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

@pytest.fixture(scope="module")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
