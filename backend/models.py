from mongoengine import (
    Document,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
)
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="staff")  # admin, staff

class Product(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    stock = IntField(required=True)
    image_url = StringField(default="")

class Sale(Document):
    product = ReferenceField(Product, required=True)
    quantity = IntField(required=True)
    total_price = FloatField(required=True)
    date = DateTimeField(default=datetime.utcnow)


class OrderItem(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    quantity = IntField(required=True)
    unit_price = FloatField(required=True)
    subtotal = FloatField(required=True)


class Order(Document):
    items = ListField(EmbeddedDocumentField(OrderItem))
    total_price = FloatField(required=True)
    date = DateTimeField(default=datetime.utcnow)
    table = StringField(default="")
    code = StringField(default="")
