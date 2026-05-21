from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from .. import models


def getTotalSpending( user_id:int, month:int, year:int, db :Session):
    total = db.query(func.coalesce(func.sum(models.Transactions.amount), 0))\
        .filter(models.Transactions.user_id == user_id)\
        .filter(models.Transactions.type == "expense")\
        .filter(extract("month", models.Transactions.created_at)== month)\
        .filter(extract("year", models.Transactions.created_at) == year)\
        .scalar() 

    return {
        "month": month,
        "year": year, 
        "total_spent": total
    }

def BudgetVsSpending(user_id:int, month:int, year:int, db:Session):
    # total budget for the month
    total_budget = db.query(func.coalesce(func.sum(models.Budget.amount),0)).filter(
        models.Budget.user_id == user_id,
        models.Budget.month == month,
        models.Budget.year == year
    ).scalar()
    
    #Get total spent in a month
    total_spent = db.query(func.coalesce(func.sum(models.Transactions.amount), 0)).filter(
        models.Transactions.user_id == user_id,
        models.Transactions.type == "expense",
        extract("month", models.Transactions.created_at) == month,
        extract("year", models.Transactions.created_at) == year
    ).scalar()
    return {
        "month": month,
        "year": year,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": total_budget - total_spent
    }

def CategoryBreakdown(user_id:int, month:int, year:int, db:Session):
    breakdown = db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Transactions.amount), 0).join(
            models.Transactions, models.Category.id == models.Transactions.category_id
        )
    ).filter(
        models.Transactions.user_id == user_id,
        extract('month', models.Transactions.created_at) == month,
        extract('year', models.Transactions.created_at) == year
    ).group_by(models.Category.name).all()
    return [{"category": name, "total_spent": total} for name, total in breakdown]

def BudgetVsCategory(user_id:int, month:int, year:int, db:Session):
    budget_category = db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Budget.amount), 0).join(
            models.Budget, models.Category.id == models.Budget.category_id
        )
    ).filter(
        models.Budget.user_id == user_id,
        models.Budget.month == month,
        models.Budget.year == year
    ).group_by(models.Category.name).all()
    
    spending_category = db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Transactions.amount), 0).join(
            models.Transactions, models.Category.id == models.Transactions.category_id
        )
    ).filter(
        models.Transactions.user_id == user_id,
        extract('month', models.Transactions.created_at) == month,
        extract('year', models.Transactions.created_at) == year
    ).group_by(models.Category.name).all()
    
    budget_dict = {name: total for name, total in budget_category}
    spending_dict = {name: total for name, total in spending_category}
    
    categories = set(budget_dict.keys()) | set(spending_dict.keys())
    
    return [{
        "category": category,
        "budget": budget_dict.get(category, 0),
        "spent": spending_dict.get(category, 0),
        "remaining": budget_dict.get(category, 0) - spending_dict.get(category, 0)
    } for category in categories]
def DailySpending(user_id:int, month:int, year:int, db:Session):
    daily_trend = db.query(
        extract('day', models.Transactions.created_at).label('day'),
        func.coalesce(func.sum(models.Transactions.amount), 0)
    ).filter(
        models.Transactions.user_id == user_id,
        models.Transactions.type == "expense",
        extract('month', models.Transactions.created_at) == month,
        extract('year', models.Transactions.created_at) == year
    ).group_by(extract('day', models.Transactions.created_at)).all()
    return [{"day": int(day), "total_spent": total} for day, total in daily_trend]
