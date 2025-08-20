from fastapi import APIRouter, HTTPException, UploadFile, File
import os
import uuid
import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate):
    new_product = models.Product(**product.dict())
    new_product.save()
    return schemas.ProductOut(
        id=str(new_product.id),
        name=new_product.name,
        price=new_product.price,
        stock=new_product.stock,
        image_url=new_product.image_url or "",
    )

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: str, product: schemas.ProductCreate):
    db_product = models.Product.objects(id=product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Keep existing image if not provided
    data = product.dict()
    if data.get("image_url") in (None, "", db_product.image_url):
        data.pop("image_url", None)
    db_product.update(**data)
    db_product.reload()
    return schemas.ProductOut(
        id=str(db_product.id),
        name=db_product.name,
        price=db_product.price,
        stock=db_product.stock,
        image_url=db_product.image_url or "",
    )

@router.delete("/{product_id}")
def delete_product(product_id: str):
    db_product = models.Product.objects(id=product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.delete()
    return {"message": "Product deleted"}


@router.get("/", response_model=list[schemas.ProductOut])
def list_products():
    items = models.Product.objects()
    return [
        schemas.ProductOut(
            id=str(p.id), name=p.name, price=p.price, stock=p.stock, image_url=p.image_url or ""
        )
        for p in items
    ]


@router.post("/{product_id}/image", response_model=schemas.ProductOut)
def upload_product_image(product_id: str, file: UploadFile = File(...)):
    db_product = models.Product.objects(id=product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    images_dir = os.path.join(os.path.dirname(__file__), "images")
    os.makedirs(images_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower()
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(images_dir, fname)

    with open(path, "wb") as f:
        f.write(file.file.read())

    rel_url = f"/static/images/{fname}"
    db_product.update(image_url=rel_url)
    db_product.reload()
    return schemas.ProductOut(
        id=str(db_product.id),
        name=db_product.name,
        price=db_product.price,
        stock=db_product.stock,
        image_url=db_product.image_url or "",
    )
