from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.analytic_crud import get_total_spending, get_total_spent, get_total_budget, category_breakdown, BudgetVsCategory, DailySpending

def _validate_month_year(month: int, year: int):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month. Must be between 1 and 12.")
    if year < 1 or year > 9999:
        raise HTTPException(status_code=400, detail="Invalid year. Must be a positive integer between 1 and 9999.")


def total_spending_service(user_id: int, month: int, year: int, db: Session):
    _validate_month_year(month, year)
    total_spent = get_total_spending(user_id=user_id, month=month, year=year, db=db)
    return {
        "month": month,
        "year": year,
        "total_spent": total_spent
    }


def budget_vs_spending_service(user_id: int, month: int, year: int, db: Session):
    _validate_month_year(month, year)
    budget = get_total_budget(user_id=user_id, month=month, year=year, db=db)
    spent = get_total_spent(user_id=user_id, month=month, year=year, db=db)
    return {
        "month": month,
        "year": year,
        "total_budget": budget,
        "total_spent": spent,
        "remaining": budget - spent
    }


def category_breakdown_service(user_id: int, month: int, year: int, db: Session):
    _validate_month_year(month, year)
    breakdown = category_breakdown(user_id=user_id, month=month, year=year, db=db)
    return {
        "month": month,
        "year": year,
        "breakdown": [
            {
                "category": name,
                "amount": total
            }
            for name, total in breakdown
        ]
    }


def budget_vs_category_service(user_id: int, month: int, year: int, db: Session):
    _validate_month_year(month, year)
    return BudgetVsCategory(user_id=user_id, month=month, year=year, db=db)
    
def daily_spending_service(user_id: int, month: int, year: int, db: Session):
    _validate_month_year(month, year)
    daily_spending = DailySpending(user_id=user_id, month=month, year=year, db=db)
    return {
        "month": month,
        "year": year,
        "daily_spending": [
                {"date": f"{year}-{month:02d}-{int(day):02d}",
                "amount": float(amount)}
            for day, amount in daily_spending
        ]
    }