from pydantic import BaseModel, EmailStr

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
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class BudgetBase(BaseModel):
    category_id: int
    amount: float
    month: str
    year: int
class BudgetCreate(BudgetBase):
    pass
class BudgetResponse(BudgetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True   