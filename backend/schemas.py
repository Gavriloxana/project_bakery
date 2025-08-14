from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    class Config:
        orm_mode = True

class SaleCreate(BaseModel):
    product_id: int
    quantity: int

class SaleOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    date: datetime
    class Config:
        orm_mode = True
