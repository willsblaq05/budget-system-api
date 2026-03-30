from fastapi import FastAPI
from app.routers import auth, register, transactions, categories, budget



app = FastAPI()
app.include_router(auth.router)
app.include_router(register.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(budget.router)

@app.get("/")
def root():
    return{"Message":"Finance API is running"}