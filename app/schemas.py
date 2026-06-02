from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password : str

class UserLogin(BaseModel):   
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type: str
    
class TokenData(BaseModel):
    id: int | None = None

class TransactionCreate(BaseModel):
    amount : float
    type : str #income or expense
    category_id: int
    description:str | None = None

class TransactionResponse(TransactionCreate):
    id : int
    user_id : int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    category_id: int
    amount: float
    month: int
    year: int
class BudgetCreate(BudgetBase):
    pass
class BudgetResponse(BudgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True   

class TotalSpendingResponse(BaseModel):
    month: int
    year : int
    total_spent : float

    class Config:
        from_attributes = True

class CategorySpending(BaseModel):
    category: str
    amount: float

class SpendingByCategoryResponse(BaseModel):
    month:int
    year:int
    breakdown: List[CategorySpending]
    class Config:
        from_attributes = True

class BudgetVsActualResponse(BaseModel):
    month : int
    year : int
    budgeted : float
    spent : float
    difference : float

    class Config:
        from_attributes = True

class BudgetVsSpendingResponse(BaseModel):
    month: int
    year: int
    total_budget: float
    total_spent: float
    remaining: float
    class Config:
        from_attributes = True

class CategoryBreakdownItem(BaseModel):
    category: str
    amount: float

class CategoryBreakdownResponse(BaseModel):
    month: int
    year: int
    breakdown: List[CategoryBreakdownItem]
    class Config:
        from_attributes = True

class BudgetVsCategoryItem(BaseModel):
    category: str
    budgeted: float
    spent: float
    difference: float

class BudgetVsCategoryResponse(BaseModel):
    month: int
    year: int
    categories: List[BudgetVsCategoryItem]
    class Config:
        from_attributes = True

class DailySpendingItem(BaseModel):
    date: str
    amount: float   

class DailySpendingResponse(BaseModel):
    month: int
    year: int
    daily_spending: List[DailySpendingItem]
    class Config:
        from_attributes = True