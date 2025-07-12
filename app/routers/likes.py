from fastapi import HTTPException, status, Depends, APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/like",
    tags=['Likes']
)

@router.post("",status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_currentuser)):
    post = db.query(models.Post).filter(models.Post.id==like.post_id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no such post exists")
    liked = db.query(models.Likes).filter(models.Likes.post_id==like.post_id, models.Likes.user_id==current_user.id)
    if like.like_dislike==1:
       if liked.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already liked the post {like.post_id}")
       new_like = models.Likes(post_id=like.post_id, user_id=current_user.id)
       db.add(new_like)
       db.commit()
       return {"message":"successfully liked the post"}
    else:
        if not liked.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote doesnt exist")
        liked.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully unliked the post"}

