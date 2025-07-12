from fastapi import HTTPException, status, Depends, APIRouter
from .. import models,schemas,utilities
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
     prefix="/users",
     tags=['Users']
)

@router.post("", status_code=status.HTTP_201_CREATED,response_model=schemas.RespondUser)
def create_user(user:schemas.UserBase,db: Session=Depends(get_db)):
        new_user=models.User(**user.model_dump())
        existing_user=db.query(models.User).filter(models.User.email==new_user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email already exists")
        new_user.password= utilities.hash_pwd(new_user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

@router.get("/{id}",response_model=schemas.RespondUser)
def view_user_details(id: int, db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user of id={id} found")
    return user

