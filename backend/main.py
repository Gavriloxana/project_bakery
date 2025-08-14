from fastapi import FastAPI
import models
from database import engine
from users import router as users_router
from products import router as products_router
from pos import router as pos_router
from reports import router as reports_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(pos_router, prefix="/pos", tags=["POS"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
