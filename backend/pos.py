from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.SaleOut)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    total_price = product.price * sale.quantity
    product.stock -= sale.quantity
    new_sale = models.Sale(product_id=product.id, quantity=sale.quantity, total_price=total_price)
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale
