from fastapi import HTTPException, status,APIRouter, Depends

from app.oauth2 import get_current_user
from .. import models, schemas
from sqlalchemy.orm import Session
from app.Database import get_db
from ..crud.CategoryCrudBreakdown import Get_Category_Breakdown

router = APIRouter(
    prefix="/category-breakdown",
    tags=["category-breakdown"]
)

@router.get("/{user_id}/{month}/{year}", response_model=schemas.CategoryBreakdownResponse)
def get_category_breakdown( month: int, year: int , db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    breakdown = Get_Category_Breakdown( current_user.id, month, year, db)
    return breakdown 