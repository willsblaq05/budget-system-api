from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from .. import models


def get_total_spending(user_id:int, month:int, year:int, db :Session):
    total = db.query(func.coalesce(func.sum(models.Transactions.amount), 0))\
        .filter(models.Transactions.user_id == user_id)\
        .filter(models.Transactions.type == "expense")\
        .filter(extract("month", models.Transactions.created_at)== month)\
        .filter(extract("year", models.Transactions.created_at) == year)\
        .scalar() 
    return total


   

def get_total_budget(user_id:int, month:int, year:int, db:Session):
    # total budget for the month
    return db.query(func.coalesce(func.sum(models.Budget.amount),0)).filter(
        models.Budget.user_id == user_id,
        models.Budget.month == month,
        models.Budget.year == year
    ).scalar()
    
def get_total_spent(user_id:int, month:int, year:int, db:Session):
    #Get total spent in a month
    return db.query(func.coalesce(func.sum(models.Transactions.amount), 0)).filter(
        models.Transactions.user_id == user_id,
        models.Transactions.type == "expense",
        extract("month", models.Transactions.created_at) == month,
        extract("year", models.Transactions.created_at) == year
    ).scalar()
   
def category_breakdown(user_id:int, month:int, year:int, db:Session):
     return db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Transactions.amount), 0)).join(
            models.Transactions, models.Category.id == models.Transactions.category_id
        ).filter(
        models.Transactions.user_id == user_id,
        extract('month', models.Transactions.created_at) == month,
        extract('year', models.Transactions.created_at) == year
    ).group_by(models.Category.name).all()
    

def BudgetVsCategory(user_id:int, month:int, year:int, db:Session):
    budget_category = db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Budget.amount), 0)).join(
            models.Budget, models.Category.id == models.Budget.category_id
        ).filter(
        models.Budget.user_id == user_id,
        models.Budget.month == month,
        models.Budget.year == year
    ).group_by(models.Category.name).all()
    
    spending_category = db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Transactions.amount), 0)).join(
            models.Transactions, models.Category.id == models.Transactions.category_id
        ).filter(
        models.Transactions.user_id == user_id,
        extract('month', models.Transactions.created_at) == month,
        extract('year', models.Transactions.created_at) == year
    ).group_by(models.Category.name).all()
    
    budget_dict = {name: total for name, total in budget_category}
    spending_dict = {name: total for name, total in spending_category}
    
    categories = set(budget_dict.keys()) | set(spending_dict.keys())
    
    
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
    