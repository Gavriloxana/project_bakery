import os
import sys
import json
from contextlib import contextmanager

MONGO_URI = "mongodb://localhost:27017/project_bakery_test"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("TESTING", "1")

import models  # type: ignore
from main import app  # type: ignore

from mongoengine import connect, disconnect
from fastapi.testclient import TestClient

@contextmanager
def test_db():
    """Switch to a dedicated test DB and clean collections."""
    # Disconnect default (in case the app already connected)
    try:
        disconnect()  # alias='default'
    except Exception:
        pass

    # Connect to test DB
    connect(host=MONGO_URI, alias="default")

    # Clean collections
    try:
        models.User.drop_collection()
    except Exception:
        pass
    try:
        models.Product.drop_collection()
    except Exception:
        pass
    try:
        models.Sale.drop_collection()
    except Exception:
        pass

    try:
        yield
    finally:
        # Optional: clean again after tests
        try:
            models.User.drop_collection()
            models.Product.drop_collection()
            models.Sale.drop_collection()
        except Exception:
            pass
        disconnect()


def pretty(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)


def expect_ok(resp, *ok_statuses):
    if not ok_statuses:
        ok_statuses = (200, 201)
    assert resp.status_code in ok_statuses, (
        f"Unexpected status {resp.status_code}:\n"
        f"{pretty(getattr(resp, 'json', lambda: resp.text)())}"
    )


def run_tests():
    results = []
    with test_db():
        client = TestClient(app)

        # --- Smoke check: docs & openapi reachable ---
        r = client.get("/docs")
        results.append(("GET /docs", r.status_code))
        r = client.get("/openapi.json")
        results.append(("GET /openapi.json", r.status_code))

        # ---------- USERS ----------
        # Create user (adjust fields if your schema differs)
        user_payload = {
            "username": "alice",
            "password": "secret123",
        }
        r = client.post("/users/", json=user_payload)
        results.append(("POST /users/", r.status_code, r.json() if r.headers.get("content-type","").startswith("application/json") else r.text))
        expect_ok(r)

        # List users
        r = client.get("/users/")
        results.append(("GET /users/", r.status_code, r.json() if r.headers.get("content-type","").startswith("application/json") else r.text))
        expect_ok(r)
        users = r.json() if r.headers.get("content-type","").startswith("application/json") else []
        user_id = None
        if isinstance(users, list) and users:
            user_id = users[0].get("id") or users[0].get("_id") or users[0].get("pk")

        # ---------- PRODUCTS ----------
        # Create a product
        product_payload = {
            "name": "Croissant",
            "price": 45.0,
            "stock": 20,
        }
        r = client.post("/products/", json=product_payload)
        results.append(("POST /products/", r.status_code, r.json() if r.headers.get("content-type","").startswith("application/json") else r.text))
        expect_ok(r)
        prod = r.json() if r.headers.get("content-type","").startswith("application/json") else {}
        product_id = prod.get("id") or prod.get("_id") or prod.get("pk")

        # Update product (price & stock)
        if product_id:
            update_payload = {"price": 50.0, "stock": 25, "name": "Croissant"}
            r = client.put(f"/products/{product_id}", json=update_payload)
            results.append((f"PUT /products/{product_id}", r.status_code, r.json() if r.headers.get("content-type","").startswith("application/json") else r.text))
            expect_ok(r)

        # ---------- POS (SALE) ----------
        # Create a sale: buy 2 croissants
        if product_id:
            sale_payload = {
                "product_id": str(product_id),
                "quantity": 2
            }
            r = client.post("/pos/", json=sale_payload)
            results.append(("POST /pos/", r.status_code, r.json() if r.headers.get("content-type","").startswith("application/json") else r.text))
            expect_ok(r)

        # ---------- DELETE PRODUCT ----------
        if product_id:
            r = client.delete(f"/products/{product_id}")
            results.append((f"DELETE /products/{product_id}", r.status_code, r.json() if r.headers.get("content-type","").startswith("application/json") else r.text))
            expect_ok(r, 200, 204)

    # Print summary
    print("\n=== TEST SUMMARY ===")
    for item in results:
        if len(item) == 2:
            name, status = item
            print(f"{name:<30} -> {status}")
        else:
            name, status, body = item
            print(f"{name:<30} -> {status}")
            try:
                print(pretty(body))
            except Exception:
                print(body)
            print("-" * 50)


if __name__ == "__main__":
    run_tests()