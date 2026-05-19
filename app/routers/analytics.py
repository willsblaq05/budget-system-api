from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..oauth2 import get_current_user
from ..Database import get_db
from ..crud.analytic_crud import getTotalSpending
from datetime import datetime

router = APIRouter(
    prefix = "/analytics",
    tags = ["Analytics"]
)

@router.get("/", response_model = schemas.TotalSpendingResponse)
def GetSpending(month:int = datetime.now().month, year:int= datetime.now().year, db: Session = Depends(get_db) , current_user : models.User=Depends(get_current_user) ):
    total_spending = getTotalSpending( current_user.id, month, year, db)
    return total_spending
