from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.service.analytic_service import total_spending_service, budget_vs_spending_service, category_breakdown_service, daily_spending_service
from .. import models, schemas
from ..oauth2 import get_current_user
from ..Database import get_db
from ..crud.analytic_crud import BudgetVsCategory

router = APIRouter(
    prefix = "/analytics",
    tags = ["Analytics"]
)

@router.get("/total_spending", response_model = schemas.TotalSpendingResponse)
def GetSpending(month:int , year:int, db: Session = Depends(get_db) , current_user : models.User=Depends(get_current_user) ):
    return total_spending_service(current_user.id, month, year, db)

@router.get("/budget_vs_spending/{month}/{year}" , response_model=schemas.BudgetVsSpendingResponse)
def GetBudgetVsSpending(month:int, year:int, db: Session = Depends(get_db) , current_user : models.User=Depends(get_current_user) ):
    return budget_vs_spending_service(current_user.id, month, year, db)

@router.get("/category_breakdown/{month}/{year}" , response_model=schemas.CategoryBreakdownResponse)
def GetCategoryBreakdown(month:int, year:int , current_user:models.User=Depends(get_current_user), db: Session = Depends(get_db) ):
    return category_breakdown_service(current_user.id, month, year, db)

@router.get("/budget_vs_category/{month}/{year}" , response_model=List[schemas.BudgetVsCategoryResponse])
def GetBudgetVsCategory(month:int, year:int , current_user:models.User=Depends(get_current_user), db: Session = Depends(get_db) ):
    budget_vs_category = BudgetVsCategory(current_user.id, month, year, db)
    return budget_vs_category
@router.get("/daily_spending/{month}/{year}", response_model=schemas.DailySpendingResponse)
def GetDailySpending(month:int, year:int , current_user:models.User=Depends(get_current_user), db: Session = Depends(get_db) ):
    return daily_spending_service(current_user.id, month, year, db)
