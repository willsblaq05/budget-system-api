from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from .. import models
#from typer import 

def get_budget_vs_spending( user_id:int, month:int, year:int, db:Session):
    # Get total budget for the month
    total_budget = db.query(func.coalesce(func.sum(models.Budget.amount), 0)).filter(
        models.Budget.user_id == user_id,
        models.Budget.month == month,
        models.Budget.year == year
        ).scalar()
    
    # Get total spending for the month
    total_spent = db.query(func.coalesce(func.sum(models.Transactions.amount), 0)).filter(
        models.Transactions.user_id == user_id,
        models.Transactions.type == "expense",
        extract(month, models.Transactions.created_at) == month,
        extract(year, models.Transactions.created_at) == year,
        ).scalar()
    return {
        "month": month,
        "year": year,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": total_budget - total_spent
    }