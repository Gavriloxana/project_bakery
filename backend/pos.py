from fastapi import APIRouter, HTTPException
import models, schemas

router = APIRouter()

@router.post("/sale", response_model=schemas.SaleOut)
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


@router.post("/checkout", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate):
    items_out: list[schemas.OrderItemOut] = []
    total_price: float = 0.0

    # Validate and prepare
    for item in order.items:
        product = models.Product.objects(id=item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found: {item.product_id}")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
        subtotal = product.price * item.quantity
        total_price += subtotal
        items_out.append(
            schemas.OrderItemOut(
                product_id=str(product.id),
                name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
                subtotal=subtotal,
            )
        )

    # Apply stock changes and persist order
    order_items_docs = []
    for out_item in items_out:
        product = models.Product.objects(id=out_item.product_id).first()
        product.stock -= out_item.quantity
        product.save()
        order_items_docs.append(
            models.OrderItem(
                product=product,
                quantity=out_item.quantity,
                unit_price=out_item.unit_price,
                subtotal=out_item.subtotal,
            )
        )

    from uuid import uuid4
    order_doc = models.Order(
        items=order_items_docs,
        total_price=total_price,
        table=order.table or "",
        code=uuid4().hex[:8]
    )
    order_doc.save()

    return schemas.OrderOut(
        id=str(order_doc.id),
        items=items_out,
        total_price=total_price,
        date=order_doc.date,
        table=order_doc.table,
    )


@router.get("/orders", response_model=list[schemas.OrderOut])
def list_orders():
    orders = models.Order.objects().order_by("-date")[:50]
    result: list[schemas.OrderOut] = []
    for o in orders:
        items: list[schemas.OrderItemOut] = []
        for itm in o.items:
            items.append(
                schemas.OrderItemOut(
                    product_id=str(itm.product.id) if itm.product else "",
                    name=itm.product.name if itm.product else "",
                    unit_price=itm.unit_price,
                    quantity=itm.quantity,
                    subtotal=itm.subtotal,
                )
            )
        result.append(
            schemas.OrderOut(
                id=str(o.id), items=items, total_price=o.total_price, date=o.date, table=o.table or ""
            )
        )
    return result


@router.get("/orders/by-table/{table}", response_model=list[schemas.OrderOut])
def orders_by_table(table: str):
    normalized = "" if (table is None or table.strip() in ("", "-", "null", "undefined")) else table
    orders = models.Order.objects(table=normalized).order_by("-date")
    result: list[schemas.OrderOut] = []
    for o in orders:
        items: list[schemas.OrderItemOut] = []
        for itm in o.items:
            items.append(
                schemas.OrderItemOut(
                    product_id=str(itm.product.id) if itm.product else "",
                    name=itm.product.name if itm.product else "",
                    unit_price=itm.unit_price,
                    quantity=itm.quantity,
                    subtotal=itm.subtotal,
                )
            )
        result.append(
            schemas.OrderOut(
                id=str(o.id), items=items, total_price=o.total_price, date=o.date, table=o.table or ""
            )
        )
    return result


@router.delete("/orders/{order_id}")
def delete_order(order_id: str):
    order = models.Order.objects(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.delete()
    return {"message": "Order deleted"}


@router.delete("/orders/by-table/{table}")
def delete_orders_by_table(table: str):
    normalized = "" if (table is None or table.strip() in ("", "-", "null", "undefined")) else table
    models.Order.objects(table=normalized).delete()
    return {"message": "Orders deleted"}
