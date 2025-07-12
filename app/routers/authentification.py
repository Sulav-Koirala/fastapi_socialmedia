from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,utilities,oauth2,schemas

router=APIRouter(
    prefix="/login",
    tags=["authentification"]
)

@router.post("",response_model=schemas.Token)
def login_user(login:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="email or password is incorrect")
    if not utilities.verify_pwd(login.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="email or password is incorrect")
    access_token = oauth2.create_accesstoken(data={"user_id":user.id})
    return {"token":access_token,
            "token_type":"bearer"}
