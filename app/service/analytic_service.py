from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.analytic_crud import get_total_spending,get_total_spent,get_total_budget,category_breakdown

def total_spending_service(user_id:int, month:int, year:int, db:Session):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month. Must be between 1 and 12.")
    if year < 1 or year > 9999:
        raise HTTPException(status_code=400, detail="Invalid year. Must be a positive integer between 1 and 9999.")
    total_spent = get_total_spending(user_id=user_id, month=month, year=year, db=db)
    return {
        "month": month,
        "year": year,
        "total_spent": total_spent

    }

def budget_vs_spending_service(user_id:int, month:int, year:int, db:Session):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month. Must be between 1 and 12.")
    if year < 1 or year > 9999:
        raise HTTPException(status_code=400, detail="Invalid year. Must be a positive integer between 1 and 9999.")
    budget = get_total_budget(user_id=user_id, month=month, year=year, db=db)
    spent = get_total_spent(user_id=user_id, month=month, year=year, db=db)
    return {
        "month": month,
        "year": year,
        "total_budget": budget,
        "total_spent": spent,
        "remaining_budget": budget - spent,
        "status": "within budget" if spent <= budget else "over budget"
    }
def category_breakdown_service(user_id:int, month:int, year:int, db:Session):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month. Must be between 1 and 12.")
    if year < 1 or year > 9999:
        raise HTTPException(status_code=400, detail="Invalid year. Must be a positive integer between 1 and 9999.")
    breakdown = category_breakdown(user_id=user_id, month=month, year=year, db=db)
    return [
        {
            "category": name,
            "total_spent": total
        }
        for name, total in breakdown
    ]