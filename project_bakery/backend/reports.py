from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db

router = APIRouter()

@router.get("/sales")
def sales_report(db: Session = Depends(get_db)):
    sales = db.query(
        func.sum(models.Sale.total_price).label("total_sales"),
        func.count(models.Sale.id).label("total_transactions")
    ).first()
    return {"total_sales": sales.total_sales or 0, "total_transactions": sales.total_transactions or 0}

@router.get("/stock")
def stock_report(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return [{"name": p.name, "stock": p.stock} for p in products]
