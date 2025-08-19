from fastapi import APIRouter, HTTPException
import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate):
    new_product = models.Product(**product.dict())
    new_product.save()
    return schemas.ProductOut(id=str(new_product.id), name=new_product.name, price=new_product.price, stock=new_product.stock)

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: str, product: schemas.ProductCreate):
    db_product = models.Product.objects(id=product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.update(**product.dict())
    db_product.reload()
    return schemas.ProductOut(id=str(db_product.id), name=db_product.name, price=db_product.price, stock=db_product.stock)

@router.delete("/{product_id}")
def delete_product(product_id: str):
    db_product = models.Product.objects(id=product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.delete()
    return {"message": "Product deleted"}
