from fastapi import APIRouter, HTTPException
import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.SaleOut)
def create_sale(sale: schemas.SaleCreate):
    product = models.Product.objects(id=sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    total_price = product.price * sale.quantity
    product.stock -= sale.quantity
    product.save()
    new_sale = models.Sale(product=product, quantity=sale.quantity, total_price=total_price)
    new_sale.save()
    return schemas.SaleOut(
        id=str(new_sale.id),
        product_id=str(product.id),
        quantity=new_sale.quantity,
        total_price=new_sale.total_price,
        date=new_sale.date
    )
