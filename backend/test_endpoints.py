import os
import sys
import json
from contextlib import contextmanager

# ใช้ DB แยกสำหรับรันเทส
MONGO_URI = "mongodb://localhost:27017/project_bakery_test"

# ให้ import โมดูลใน backend ได้
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# flag เฉพาะสภาพแวดล้อมเทส
os.environ.setdefault("TESTING", "1")

import models  # type: ignore
from main import app  # type: ignore

from mongoengine import connect, disconnect
from fastapi.testclient import TestClient


@contextmanager
def test_db():
    """สลับมาใช้ Test DB และล้าง collections ก่อน-หลังรัน"""
    try:
        disconnect()
    except Exception:
        pass

    connect(host=MONGO_URI, alias="default")

    for coll in (models.User, models.Product, models.Sale, models.Order):
        try:
            coll.drop_collection()
        except Exception:
            pass

    try:
        yield
    finally:
        for coll in (models.User, models.Product, models.Sale, models.Order):
            try:
                coll.drop_collection()
            except Exception:
                pass
        disconnect()


def pretty(obj):
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def is_json(resp):
    return resp.headers.get("content-type", "").startswith("application/json")


def j(resp, default=None):
    if is_json(resp):
        try:
            return resp.json()
        except Exception:
            return default
    return default


def expect_ok(resp, *ok_statuses):
    if not ok_statuses:
        ok_statuses = (200, 201)
    assert resp.status_code in ok_statuses, (
        f"Unexpected status {resp.status_code}:\n"
        f"{pretty(getattr(resp, 'json', lambda: resp.text)())}"
    )


def add_result(results, name, resp, expect_statuses=None):
    payload = j(resp, resp.text)
    results.append((name, resp.status_code, payload))
    if expect_statuses:
        assert resp.status_code in expect_statuses, (
            f"{name} -> expected {expect_statuses}, got {resp.status_code}\n{pretty(payload)}"
        )


def run_tests():
    results = []
    defects = []  # เก็บเคสที่ backend ควรปฏิเสธแต่ตอนนี้ยังปล่อย (ไม่ทำให้เทสล้ม)

    with test_db():
        client = TestClient(app)

        # --- Smoke check: docs & openapi reachable ---
        r = client.get("/docs")
        results.append(("GET /docs", r.status_code))
        r = client.get("/openapi.json")
        results.append(("GET /openapi.json", r.status_code))

        # ---------- USERS ----------
        # Create user
        user_payload = {"username": "alice", "password": "secret123"}
        r = client.post("/users/", json=user_payload)
        add_result(results, "POST /users/", r, expect_statuses=(200, 201))

        # Duplicate username should fail (ถ้าระบบบล็อกถูกต้องจะได้ 400)
        r = client.post("/users/", json=user_payload)
        if r.status_code != 400:
            defects.append(("Duplicate username accepted", r.status_code, j(r, r.text)))
        else:
            results.append(("POST /users/ (duplicate) -> 400", r.status_code, j(r, r.text)))

        # List users
        r = client.get("/users/")
        add_result(results, "GET /users/", r, expect_statuses=(200,))
        users = j(r, []) or []
        user_id = None
        if isinstance(users, list) and users:
            user_id = users[0].get("id") or users[0].get("_id") or users[0].get("pk")

        # ---------- PRODUCTS ----------
        # Create product A (หลัก ใช้ทดสอบ flow จริง)
        productA_payload = {"name": "Croissant", "price": 45.0, "stock": 20}
        r = client.post("/products/", json=productA_payload)
        add_result(results, "POST /products/ (A)", r, expect_statuses=(200, 201))
        prodA = j(r, {}) or {}
        productA_id = prodA.get("id") or prodA.get("_id") or prodA.get("pk")

        # Update product A (price & stock)
        if productA_id:
            update_payload = {"name": "Croissant", "price": 50.0, "stock": 25}
            r = client.put(f"/products/{productA_id}", json=update_payload)
            add_result(results, f"PUT /products/{productA_id}", r, expect_statuses=(200,))

        # List products (should have >=1)
        r = client.get("/products/")
        add_result(results, "GET /products/", r, expect_statuses=(200,))

        # Validation soft-check: negative price / stock (ควร 400 ถ้า validate)
        bad_prod_payloads = [
            {"name": "BadPrice", "price": -1, "stock": 5},
            {"name": "BadStock", "price": 10, "stock": -5},
        ]
        for pld in bad_prod_payloads:
            r = client.post("/products/", json=pld)
            if r.status_code != 400:
                defects.append(("Product invalid value accepted", r.status_code, {"payload": pld, "resp": j(r, r.text)}))
            else:
                results.append(("POST /products/ (invalid) -> 400", r.status_code, j(r, r.text)))

        # ---------- PRODUCT IMAGE UPLOAD ----------
        if productA_id:
            # อัปโหลดไฟล์ภาพจำลอง (jpg)
            files = {
                "file": ("test.jpg", b"\xff\xd8\xff\xdbFAKEJPEGDATA", "image/jpeg")
            }
            r = client.post(f"/products/{productA_id}/image", files=files)
            add_result(results, f"POST /products/{productA_id}/image", r, expect_statuses=(200,))
            body = j(r, {}) or {}
            img_url = body.get("image_url")
            if img_url:
                # ลอง GET รูปที่ mount ไว้
                r2 = client.get(img_url)
                # StaticFiles จะตอบ 200 ถ้าไฟล์มีจริง
                if r2.status_code != 200:
                    defects.append(("Image URL not accessible", r2.status_code, {"url": img_url, "resp": r2.text}))

        # ---------- POS (SALE) : flow จริงบน product A ----------
        if productA_id:
            # Sale: buy 2 croissants (ราคาอัปเดตเป็น 50 แล้ว)
            sale_payload = {"product_id": str(productA_id), "quantity": 2}
            r = client.post("/pos/sale", json=sale_payload)
            add_result(results, "POST /pos/sale", r, expect_statuses=(200, 201))

            # ตรวจ stock ลดลง 2: 25 -> 23
            r = client.get("/products/")
            expect_ok(r)
            products = j(r, []) or []
            afterA = next(p for p in products if p["id"] == productA_id)
            assert afterA["stock"] == 23, f"expected stock=23 after sale, got {afterA['stock']}"

        # ---------- POS (CHECKOUT & ORDERS) : ใช้ product A + สร้าง product B ----------
        # สร้าง product B เพิ่มสำหรับ checkout หลายรายการ
        productB_payload = {"name": "Brownie", "price": 30.0, "stock": 50}
        r = client.post("/products/", json=productB_payload)
        add_result(results, "POST /products/ (B)", r, expect_statuses=(200, 201))
        prodB = j(r, {}) or {}
        productB_id = prodB.get("id") or prodB.get("_id") or prodB.get("pk")

        orderA_id = None
        if productA_id and productB_id:
            # Checkout #1 (table=A1): Croissant x3 + Brownie x4
            checkout_payload = {
                "items": [
                    {"product_id": str(productA_id), "quantity": 3},
                    {"product_id": str(productB_id), "quantity": 4},
                ],
                "table": "A1",
            }
            r = client.post("/pos/checkout", json=checkout_payload)
            add_result(results, "POST /pos/checkout (A1)", r, expect_statuses=(200, 201))
            orderA = j(r, {}) or {}
            orderA_id = orderA.get("id")

            # ตรวจ total_price (50*3 + 30*4 = 150 + 120 = 270)
            assert abs(orderA.get("total_price", -999) - 270.0) < 1e-6, f"total_price mismatch: {orderA}"

            # ตรวจ stock หลัง checkout: Croissant 23 -> 20, Brownie 50 -> 46
            r = client.get("/products/")
            expect_ok(r)
            products_now = j(r, []) or []
            pa = next(p for p in products_now if p["id"] == productA_id)
            pb = next(p for p in products_now if p["id"] == productB_id)
            assert pa["stock"] == 20, f"Croissant stock mismatch after checkout: {pa['stock']}"
            assert pb["stock"] == 46, f"Brownie stock mismatch after checkout: {pb['stock']}"

            # Checkout #2 (table=""): Brownie x1
            checkout2_payload = {
                "items": [{"product_id": str(productB_id), "quantity": 1}],
                "table": ""
            }
            r = client.post("/pos/checkout", json=checkout2_payload)
            add_result(results, "POST /pos/checkout (blank table)", r, expect_statuses=(200, 201))

            # Orders listing
            r = client.get("/pos/orders")
            add_result(results, "GET /pos/orders", r, expect_statuses=(200,))
            orders_all = j(r, []) or []
            assert len(orders_all) >= 2, f"expected >=2 orders, got {len(orders_all)}"

            # by-table A1 => ต้องมี orderA
            r = client.get("/pos/orders/by-table/A1")
            add_result(results, "GET /pos/orders/by-table/A1", r, expect_statuses=(200,))
            orders_A1 = j(r, []) or []
            assert any(o.get("id") == orderA_id for o in orders_A1), "order A1 not found in by-table A1"

            # by-table "undefined" => ต้องดึง table="" ได้ (normalization)
            r = client.get("/pos/orders/by-table/undefined")
            add_result(results, "GET /pos/orders/by-table/undefined", r, expect_statuses=(200,))
            orders_blank = j(r, []) or []
            assert len(orders_blank) >= 1, "expected orders for blank/undefined table"

            # DELETE order A1 by id
            if orderA_id:
                r = client.delete(f"/pos/orders/{orderA_id}")
                add_result(results, f"DELETE /pos/orders/{orderA_id}", r, expect_statuses=(200,))
                # ควรไม่เหลือใน by-table A1
                r = client.get("/pos/orders/by-table/A1")
                expect_ok(r)
                assert not any(o.get("id") == orderA_id for o in j(r, []) or []), "order still present after delete"

            # DELETE orders by-table "" (ใช้ keyword 'undefined' แทน)
            r = client.delete("/pos/orders/by-table/undefined")
            add_result(results, "DELETE /pos/orders/by-table/undefined", r, expect_statuses=(200,))
            r = client.get("/pos/orders/by-table/undefined")
            expect_ok(r)
            assert len(j(r, []) or []) == 0, "blank table orders not deleted"

        # ---------- POS (VALIDATION ON SEPARATE PRODUCT) ----------
        # เพื่อไม่ให้ state ของสินค้าหลักเพี้ยน เราสร้าง product แยกสำหรับทดสอบ quantity ผิดปกติ
        validator_payload = {"name": "ValidatorItem", "price": 10.0, "stock": 10}
        r = client.post("/products/", json=validator_payload)
        add_result(results, "POST /products/ (ValidatorItem)", r, expect_statuses=(200, 201))
        vprod = j(r, {}) or {}
        vprod_id = vprod.get("id") or vprod.get("_id") or vprod.get("pk")

        if vprod_id:
            # Negative quantity (ควร 400)
            bad_sale = {"product_id": str(vprod_id), "quantity": -1}
            r = client.post("/pos/sale", json=bad_sale)
            if r.status_code != 400:
                defects.append(("Sale negative quantity accepted", r.status_code, j(r, r.text)))
            else:
                results.append(("POST /pos/sale (negative qty) -> 400", r.status_code, j(r, r.text)))

            # Zero quantity (ควร 400 เช่นกัน)
            zero_sale = {"product_id": str(vprod_id), "quantity": 0}
            r = client.post("/pos/sale", json=zero_sale)
            if r.status_code != 400:
                defects.append(("Sale zero quantity accepted", r.status_code, j(r, r.text)))
            else:
                results.append(("POST /pos/sale (zero qty) -> 400", r.status_code, j(r, r.text)))

        # ---------- REPORTS ----------
        r = client.get("/reports/sales")
        add_result(results, "GET /reports/sales", r, expect_statuses=(200,))
        sales_rep = j(r, {}) or {}
        # ตอนนี้ reports/sales นับเฉพาะ Sale (ไม่รวมหรือเด้งกับ Orders)
        # เราสร้าง sale 1 ครั้ง (2 ชิ้น * 50) => total_transactions ควร >=1, total_sales >=100
        if sales_rep.get("total_transactions", 0) < 1 or sales_rep.get("total_sales", 0.0) < 100.0:
            defects.append(("Sales report likely ignores Orders (by design)", 200, sales_rep))
        else:
            results.append(("REPORTS sales baseline ok", 200, sales_rep))

        r = client.get("/reports/stock")
        add_result(results, "GET /reports/stock", r, expect_statuses=(200,))
        stock_list = j(r, []) or []
        # หลังจากลบ orders ไปแล้ว stock ไม่คืน (ตามโค้ดปัจจุบัน)
        # ณ จุดนี้ Croissant ควรเหลือ 20, Brownie เหลือ 45 (ลดเพิ่มจาก checkout2 อีก 1)
        names = {p["name"]: p["stock"] for p in stock_list if "name" in p}
        if "Croissant" in names and "Brownie" in names:
            if names["Croissant"] != 20 or names["Brownie"] != 45:
                defects.append(("Stock numbers mismatch (check flow)", 200, names))

                # ---------- NEGATIVE / ERROR-PATH TESTS ----------

        # 1) Validation: missing fields / wrong types -> 422 (Pydantic)
        r = client.post("/products/", json={})  # ไม่มี name/price/stock
        add_result(results, "POST /products/ (missing fields)", r, expect_statuses=(422,))

        r = client.post("/products/", data="not json", headers={"Content-Type": "application/json"})
        add_result(results, "POST /products/ (malformed JSON)", r, expect_statuses=(422,))

        r = client.post("/products/", json={"name": "WrongType", "price": "xx", "stock": "yy"})
        add_result(results, "POST /products/ (wrong types)", r, expect_statuses=(422,))

        # 2) Nonexistent IDs -> 404
        bad_id = "000000000000000000000000"  # รูปแบบ ObjectId 24 hex
        r = client.put(f"/products/{bad_id}", json={"name": "X", "price": 1, "stock": 1})
        add_result(results, f"PUT /products/{bad_id} (not found)", r, expect_statuses=(404,))

        r = client.delete(f"/products/{bad_id}")
        add_result(results, f"DELETE /products/{bad_id} (not found)", r, expect_statuses=(404,))

        r = client.post("/pos/sale", json={"product_id": bad_id, "quantity": 1})
        add_result(results, "POST /pos/sale (nonexistent product)", r, expect_statuses=(404,))

        # 3) Insufficient stock -> 400
        # สร้าง product C สำหรับทดสอบสต็อกไม่พอ
        r = client.post("/products/", json={"name": "TinyStock", "price": 9.0, "stock": 1})
        add_result(results, "POST /products/ (TinyStock)", r, expect_statuses=(200, 201))
        prodC = j(r, {}) or {}
        productC_id = prodC.get("id") or prodC.get("_id") or prodC.get("pk")

        if productC_id:
            # sale มากกว่าสต็อก
            r = client.post("/pos/sale", json={"product_id": str(productC_id), "quantity": 2})
            add_result(results, "POST /pos/sale (insufficient stock)", r, expect_statuses=(400,))

            # checkout มากกว่าสต็อก
            r = client.post("/pos/checkout", json={"items": [{"product_id": str(productC_id), "quantity": 2}]})
            add_result(results, "POST /pos/checkout (insufficient stock)", r, expect_statuses=(400,))

            # sequential oversell: ซื้อ 1 ครั้งแรกผ่าน, ครั้งที่สองควร 400
            r = client.post("/pos/checkout", json={"items": [{"product_id": str(productC_id), "quantity": 1}]})
            add_result(results, "POST /pos/checkout (TinyStock first 1)", r, expect_statuses=(200, 201))
            r = client.post("/pos/checkout", json={"items": [{"product_id": str(productC_id), "quantity": 1}]})
            add_result(results, "POST /pos/checkout (TinyStock second 1 -> 400)", r, expect_statuses=(400,))

        # 4) Checkout with empty items -> ควร 400 (ถ้าธุรกิจไม่ยอมออเดอร์ว่าง)
        r = client.post("/pos/checkout", json={"items": [], "table": "Z9"})
        if r.status_code != 400:
            defects.append(("Checkout with empty items accepted", r.status_code, j(r, r.text)))
        else:
            results.append(("POST /pos/checkout (empty items) -> 400", r.status_code, j(r, r.text)))

        # 5) Delete order with nonexistent id -> 404
        r = client.delete("/pos/orders/000000000000000000000000")
        add_result(results, "DELETE /pos/orders/<bad_id>", r, expect_statuses=(404,))

        # 6) Image upload invalid type / huge size -> ควร 400
        if productA_id:
            files_bad = {"file": ("bad.exe", b"MZfake", "application/octet-stream")}
            r = client.post(f"/products/{productA_id}/image", files=files_bad)
            # ถ้ายังไม่กรองชนิดไฟล์ ให้ขึ้น defect
            if r.status_code != 400:
                defects.append(("Image upload: invalid type accepted", r.status_code, j(r, r.text)))
            else:
                results.append(("POST /products/{id}/image (invalid ext) -> 400", r.status_code, j(r, r.text)))

            # ไฟล์ใหญ่ผิดปกติ (1*1024*1024 ~ 1MB; ปรับตามนโยบายที่ทีมอยากได้)
            big_data = b"x" * (6 * 1024 * 1024)  # 6MB
            files_big = {"file": ("big.jpg", big_data, "image/jpeg")}
            r = client.post(f"/products/{productA_id}/image", files=files_big)
            if r.status_code != 400:
                defects.append(("Image upload: oversized accepted", r.status_code, {"len": len(big_data), "resp": j(r, r.text)}))
            else:
                results.append(("POST /products/{id}/image (oversized) -> 400", r.status_code, j(r, r.text)))


        # ---------- DELETE PRODUCTS ----------
        if productA_id:
            r = client.delete(f"/products/{productA_id}")
            add_result(results, f"DELETE /products/{productA_id}", r, expect_statuses=(200, 204))
        if productB_id:
            r = client.delete(f"/products/{productB_id}")
            add_result(results, f"DELETE /products/{productB_id}", r, expect_statuses=(200, 204))
        if vprod_id:
            r = client.delete(f"/products/{vprod_id}")
            add_result(results, f"DELETE /products/{vprod_id}", r, expect_statuses=(200, 204))

    # Print summary
    print("\n=== TEST SUMMARY ===")
    for item in results:
        if len(item) == 2:
            name, status = item
            print(f"{name:<40} -> {status}")
        else:
            name, status, body = item
            print(f"{name:<40} -> {status}")
            try:
                print(pretty(body))
            except Exception:
                print(body)
            print("-" * 50)

    if defects:
        print("\n=== DEFECTS (should fix in backend) ===")
        for name, status, body in defects:
            print(f"{name:<40} -> {status}")
            print(pretty(body))
            print("-" * 50)


if __name__ == "__main__":
    run_tests()
