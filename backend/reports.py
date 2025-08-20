from fastapi import APIRouter
import models

router = APIRouter()


@router.get("/sales")
def sales_report():
    total_sales = 0.0
    total_transactions = 0
    sales = models.Sale.objects()
    total_transactions = sales.count()
    total_sales = sum(s.total_price for s in sales)
    return {"total_sales": total_sales, "total_transactions": total_transactions}


@router.get("/stock")
def stock_report():
    products = models.Product.objects()
    return [{"name": p.name, "stock": p.stock} for p in products]
