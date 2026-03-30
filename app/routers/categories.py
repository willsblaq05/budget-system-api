from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..crud import category_crud
from app.Database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
    )
@router.post("/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return category_crud.create_category(db, category, current_user.id)

@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return category_crud.get_categories(db, current_user.id)