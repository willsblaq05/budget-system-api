from sqlalchemy import Column, Integer,Float,String, DateTime, ForeignKey
from datetime import datetime
from .Database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index =True)
    email = Column(String , unique = True , nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transactions", back_populates="user")
    categories = relationship("Category", back_populates="user")
class Transactions(Base):
    __tablename__ = "transactions"    

    id = Column(Integer, primary_key = True, index= True)
    amount = Column(Float, nullable = False)
    type = Column(String, nullable = False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates ="transactions")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="transactions")
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="categories")

    transactions = relationship("Transactions", back_populates="category")

    