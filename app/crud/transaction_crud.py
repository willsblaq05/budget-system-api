from sqlalchemy.orm import Session

from app.crud.category_crud import get_category_or_404
from .. import models, schemas
from fastapi import HTTPException, status
from .. import models, schemas
from app.crud.category_crud import get_category_or_404
def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id:int):
     # 🔥 Validate category
    category = get_category_or_404(  db, transaction.category_id)

    new_transaction = models.Transactions(**transaction.dict(), user_id=user_id)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_transactions(db:Session, user_id:int):
    return db.query(models.Transactions).filter(models.Transactions.user_id == user_id).all()