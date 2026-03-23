from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    db_category = models.Category(name=category.name, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
def get_categories(db: Session, user_id: int):
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()   

def get_category_or_404(db:Session, category_id:int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category or category.user_id :
        raise HTTPException(status_code=404, detail="Category not found")
    return category
        