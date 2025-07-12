from pydantic import BaseModel,EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

class RespondUser(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title:str
    content:str
    post:bool = True
    rating:Optional[int] = None

class Response(PostBase):
    id: int
    created_at:datetime
    owner: RespondUser

    class Config:
        from_attributes = True

class ResponseLikes(BaseModel):
    Post: Response
    likes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    token:str
    token_type:str

class TokenData(BaseModel):
    id: int

class Like(BaseModel):
    post_id: int
    like_dislike: Annotated[int, Field(ge=0, le=1)]
