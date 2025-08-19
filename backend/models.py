from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="staff")  # admin, staff

class Product(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    stock = IntField(required=True)

class Sale(Document):
    product = ReferenceField(Product, required=True)
    quantity = IntField(required=True)
    total_price = FloatField(required=True)
    date = DateTimeField(default=datetime.utcnow)
