from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from . import schemas,database,models
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire

def create_accesstoken(data: dict):
    to_encode = data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_accesstoken(token: str, exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        token_data = schemas.TokenData(id=id)
        if id == None:
            raise exception
    except JWTError:
        raise exception
    return token_data

def get_currentuser(token: str = Depends(oauth2_scheme),db: Session=Depends(database.get_db)):
    exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    verify = verify_accesstoken(token,exception)
    user = db.query(models.User).filter(models.User.id == verify.id).first()
    return user
