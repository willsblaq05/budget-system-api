from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..oauth2 import get_current_user
from ..Database import get_db
from ..crud.analytic_crud import getTotalSpending, CategoryBreakdown, BudgetVsSpending, BudgetVsCategory, DailySpending
from datetime import datetime

router = APIRouter(
    prefix = "/analytics",
    tags = ["Analytics"]
)

@router.get("/total_spending", response_model = schemas.TotalSpendingResponse)
def GetSpending(month:int = datetime.now().month, year:int= datetime.now().year, db: Session = Depends(get_db) , current_user : models.User=Depends(get_current_user) ):
    total_spending = getTotalSpending( current_user.id, month, year, db)
    return total_spending
@router.get("/budget_vs_spending/{month}/{year}" , response_model=schemas.BudgetVsSpendingResponse)
def GetBudgetVsSpending(month:int, year:int, db: Session = Depends(get_db) , current_user : models.User=Depends(get_current_user) ):
    Budget_vs_Spending = BudgetVsSpending(current_user.id, month, year, db)
    return Budget_vs_Spending
@router.get("/category_breakdown/{month}/{year}" , response_model=schemas.CategoryBreakdownResponse)
def GetCategoryBreakdown(month:int, year:int , current_user:models.User=Depends(get_current_user), db: Session = Depends(get_db) ):
    category_breakdown = CategoryBreakdown(current_user.id, month, year, db)
    return category_breakdown
@router.get("/budget_vs_category/{month}/{year}" , response_model=schemas.BudgetVsCategoryResponse)
def GetBudgetVsCategory(month:int, year:int , current_user:models.User=Depends(get_current_user), db: Session = Depends(get_db) ):
    budget_vs_category = BudgetVsCategory(current_user.id, month, year, db)
    return budget_vs_category
def GetDailySpending(month:int, year:int , current_user:models.User=Depends(get_current_user), db: Session = Depends(get_db) ):
    daily_spending = DailySpending(current_user.id, month, year, db)
    return daily_spending