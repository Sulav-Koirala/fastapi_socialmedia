from fastapi import HTTPException, status, Depends, APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("", response_model=List[schemas.ResponseLikes])
def get_posts(db:Session=Depends(get_db), current_user: str=Depends(oauth2.get_currentuser), limit:int = 10, skip: int =0, search: Optional[str]=""):
    posts=db.query(models.Post, func.count(models.Likes.post_id).label("likes")).join(models.Likes,models.Likes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def post_data(post:schemas.PostBase, db:Session=Depends(get_db), current_user: str=Depends(oauth2.get_currentuser)):
    posts=models.Post(user_id=current_user.id,**post.model_dump())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

@router.get("/{id}",response_model=schemas.Response)
def get_post(id: int, db:Session=Depends(get_db), current_user: str=Depends(oauth2.get_currentuser)):
    posts=db.query(models.Post).filter(models.Post.id==id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such post with id={id} exists")
    return posts

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int, db:Session=Depends(get_db), current_user: str=Depends(oauth2.get_currentuser)):
    posts=db.query(models.Post).filter(models.Post.id==id)
    if posts.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such post with id={id} exists")
    if posts.first().user_id != current_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,detail="you cant delete someone elses post")
    posts.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}",response_model=schemas.Response)
def update_post(id:int, update:schemas.PostBase, db:Session=Depends(get_db), current_user: str=Depends(oauth2.get_currentuser)):
    posts=db.query(models.Post).filter(models.Post.id==id)
    if posts.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such post with id={id} exists")
    if posts.first().user_id != current_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,detail="you cant update someone elses post")
    posts.update(update.model_dump(),synchronize_session=False)
    db.commit()
    return posts.first()
