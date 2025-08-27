import os
from mongoengine import connect
from dotenv import load_dotenv

# โหลดค่า .env
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB   = os.getenv("MONGO_DB")
MONGO_AUTH = os.getenv("MONGO_AUTH_DB")

# สร้าง URI (เข้ารหัสรหัสผ่านอัตโนมัติถ้ามีอักขระพิเศษ)
from urllib.parse import quote_plus
MONGO_PASS_ENC = quote_plus(MONGO_PASS)

uri = f"mongodb://{MONGO_USER}:{MONGO_PASS_ENC}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_AUTH}"

connect(db=MONGO_DB, host=uri)
