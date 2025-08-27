from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from users import router as users_router
from products import router as products_router
from pos import router as pos_router
from reports import router as reports_router
import database  # ensure Mongo connectionnnn

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8100",
    "http://localhost:8000",
    "http://localhost:8100",
    "http://192.168.10.118:8000",
    "http://192.168.10.118:8100",
    "https://api-bakery.loeitech.org",
    "https://bakery.loeitech.org"
    

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for product images
static_images_dir = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(static_images_dir, exist_ok=True)
app.mount("/static/images", StaticFiles(directory=static_images_dir), name="images")

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(pos_router, prefix="/pos", tags=["POS"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
