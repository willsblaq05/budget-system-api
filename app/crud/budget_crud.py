from fastapi import HTTPException,Depends, status
from sqlalchemy.orm import Session
from app.Database import get_db
from .. import models, schemas

def create_budget(db: Session, budget: schemas.BudgetCreate, user_id:int):
    new_budget = models.Budget(**budget.dict(), user_id=user_id)
    db.add(new_budget)
    db.commit() 
    db.refresh(new_budget)
    return new_budget

def get_budgets(db: Session, user_id:int):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()