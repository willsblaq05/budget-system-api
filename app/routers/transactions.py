from fastapi import APIRouter,Depends,HTTPException, status
from sqlalchemy.orm import Session
from app.Database import get_db
from .. import models, schemas
from app.oauth2 import get_current_user
from ..crud.category_crud import get_category_or_404
from ..crud.transaction_crud import create_transaction, get_transactions    

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

#Create transaction
@router.post("/", response_model=schemas.TransactionResponse)
def make_transaction(transaction:schemas.TransactionCreate,
                      db : Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):
     # 🔥 Validate category
    
    return get_category_or_404(db, transaction.category_id)  # This will raise a 404 if the category doesn't exist or doesn't belong to the user
#Get all transacctions for current user

@router.get("/", response_model=list[schemas.TransactionResponse])
def get_transactions(db: Session = Depends(get_db), current_user :models.User = Depends(get_current_user)):
    return get_transactions(db, current_user.id)

#Delete a transaction
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db:Session=Depends(get_db), current_user:models.User = Depends(get_current_user)):
    transaction = db.query(models.Transactions).filter(models.Transactions.id == transaction_id, models.Transactions.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted"}

    




