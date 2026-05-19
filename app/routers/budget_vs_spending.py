from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Database import get_db
from app import models, schemas
from app.crud.get_budgetVsSpending_crud import get_budget_vs_spending
from app.oauth2 import get_current_user
router = APIRouter(
    prefix="/budget_vs_spending",
    tags=["Budget vs Spending"]
)
@router.get("/{month}/{year}", response_model=schemas.BudgetVsSpendingResponse)
def budget_vs_spending(month: int, year: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return get_budget_vs_spending( current_user.id, month, year, db)