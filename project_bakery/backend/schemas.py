from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Users
class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "staff"

class UserOut(BaseModel):
    id: str
    username: str
    role: str

# Products
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    stock: int

# Sales
class SaleCreate(BaseModel):
    product_id: str
    quantity: int

class SaleOut(BaseModel):
    id: str
    product_id: str
    quantity: int
    total_price: float
    date: datetime
