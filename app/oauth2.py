from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, Database
from .schemas import TokenData   
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(
        token: str = Depends(oauth2_scheme),db:Session = Depends(Database.get_db)):
        credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials")

        try:
              payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

              user_id = payload.get("user_id")

              if user_id is None:
                    raise credential_exception
              
              token_data = TokenData(id = user_id)
        except JWTError:
              raise credential_exception
        
        user = db.query(models.User).filter(models.User.id == token_data.id).first()

        return user

