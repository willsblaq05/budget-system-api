from sqlalchemy.orm import Session
from .. import models
from sqlalchemy import func, extract

def Get_Category_Breakdown( user:int, month:int, year:int, db:Session):
    breakdown = db.query(
        models.Category.name,
        func.coalesce(func.sum(models.Transactions.amount), 0).join(
            models.Transactions, models.Category.id == models.Transactions.category_id
        )
    ).filter(
        models.Transactions.user_id == user,
        extract('month', models.Transactions.created_at) == month,
        extract('year', models.Transactions.created_at) == year
    ).group_by(models.Category.name).all()
    return [{"category": name, "total_spent": total} for name, total in breakdown]