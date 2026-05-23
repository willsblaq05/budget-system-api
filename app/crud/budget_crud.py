from fastapi import HTTPException,Depends, status
from sqlalchemy.orm import Session
from app.Database import get_db
from .. import models, schemas
from app.crud.category_crud import get_category_or_404

def create_budget( user_id:int, db: Session, budget: schemas.BudgetCreate):
    # Validate category
    get_category_or_404(db, budget.category_id)
    new_budget = models.Budget(**budget.dict(), user_id=user_id)
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

def get_budgets(user_id:int ,db: Session):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()