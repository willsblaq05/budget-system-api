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