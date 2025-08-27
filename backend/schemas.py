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
    class Config:
        from_attributes = True

# Products
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    stock: int
    image_url: str
    class Config:
        from_attributes = True

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
    class Config:
        from_attributes = True


# Orders
class OrderItemIn(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemIn]
    table: Optional[str] = ""


class OrderItemOut(BaseModel):
    product_id: str
    name: str
    unit_price: float
    quantity: int
    subtotal: float


class OrderOut(BaseModel):
    id: str
    items: list[OrderItemOut]
    total_price: float
    date: datetime
    table: str
    class Config:
        from_attributes = True
