from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#import os

#sqlalchemy_db_url=os.getenv("DATABASE_URL")
#if not sqlalchemy_db_url:
sqlalchemy_db_url=f"postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
engine=create_engine(sqlalchemy_db_url)
session_local=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()
