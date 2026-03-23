from fastapi import HTTPException,APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.oauth2 import create_access_token
from ..Database import get_db
from .. import models, utils,schemas
router =APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/", response_model=schemas.Token)
def login(user: schemas.UserLogin, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = create_access_token(data={"user_id": db_user.id})
    return{
        "access_token":access_token,
        "token_type":"bearer"
    }
