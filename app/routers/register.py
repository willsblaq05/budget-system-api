from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..import models, schemas, utils
from ..Database import get_db

router = APIRouter(
    prefix="/register",
    tags=["Register"]
)
#Register users
@router.post("/")
def register(user: schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




    