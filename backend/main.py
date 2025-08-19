from fastapi import FastAPI
from users import router as users_router
from products import router as products_router
from pos import router as pos_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(pos_router, prefix="/pos", tags=["POS"])
