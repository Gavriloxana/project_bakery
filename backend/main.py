from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from users import router as users_router
from products import router as products_router
from pos import router as pos_router
from reports import router as reports_router
import database  # ensure Mongo connection

app = FastAPI()

# ✅ Allow all hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for product images
static_images_dir = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(static_images_dir, exist_ok=True)
app.mount("/static/images", StaticFiles(directory=static_images_dir), name="images")

# Routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(pos_router, prefix="/pos", tags=["POS"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
