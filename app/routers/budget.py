from fastapi import APIRouter,Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas
from app.Database import get_db
from app.oauth2 import get_current_user
from ..crud import budget_crud
from ..crud.category_crud import get_category_or_404

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"]
)

@router.post("/")
def create_budget( budget: schemas.BudgetCreate ,db:Session =Depends(get_db), current_user: models.User = Depends(get_current_user)):
    category = get_category_or_404(db, budget.category_id)
    return budget_crud.create_budget(current_user.id, db, budget)

@router.get("/get", response_model=list[schemas.BudgetResponse])
def GetBudgets(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return budget_crud.get_budgets( current_user.id, db)