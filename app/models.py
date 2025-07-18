from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    rating=Column(Integer, nullable=True)
    post=Column(Boolean,nullable=False,server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    user_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class Likes(Base):
    __tablename__="likes_post"
    user_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)