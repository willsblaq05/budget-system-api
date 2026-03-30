from fastapi import APIRouter,Depends,HTTPException, status
from sqlalchemy.orm import Session
from app.Database import get_db
from .. import models, schemas
from app.oauth2 import get_current_user
from ..crud.category_crud import get_category_or_404
from ..crud import transaction_crud 

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

#Create transaction
@router.post("/", response_model=schemas.TransactionResponse)
def make_transaction(transaction:schemas.TransactionCreate,
                      db : Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):

    return transaction_crud.create_transaction(db, transaction, current_user.id)
#Get all transactions for current user

@router.get("/", response_model=list[schemas.TransactionResponse])
def get_transactions(db: Session = Depends(get_db), current_user :models.User = Depends(get_current_user)):
    return transaction_crud.get_transactions(db, current_user.id)

#Delete a transaction
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db:Session=Depends(get_db), current_user:models.User = Depends(get_current_user)):
    transaction = db.query(models.Transactions).filter(models.Transactions.id == transaction_id, models.Transactions.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted"}

    




