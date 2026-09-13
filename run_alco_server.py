#!/usr/bin/env python3
"""
Alco Ecommerce Standalone & Frappe Web Server
Serves Alco Ecommerce frontend & backend APIs on port 8080.
"""

import ast
import http.server
import json
import os
import socketserver
import sys
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "alco_ecommerce", "alco_ecommerce"))
sys.path.insert(0, os.path.join(BASE_DIR, "alco_ecommerce"))
from dynamic_gradient import extract_dynamic_gradient

WWW_DIR = os.path.join(BASE_DIR, "alco_ecommerce", "alco_ecommerce", "www")
PUBLIC_DIR = os.path.join(BASE_DIR, "alco_ecommerce", "alco_ecommerce", "public")
API_PY = os.path.join(BASE_DIR, "alco_ecommerce", "alco_ecommerce", "api.py")
DATA_DIR = os.path.join(BASE_DIR, "data")
ORDERS_FILE = os.path.join(DATA_DIR, "orders_db.json")

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. LOAD CATALOG & DEPOTS FROM API.PY
# -------------------------------------------------------------
catalog = []
depots = []
try:
    with open(API_PY, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == "ALCO_CATALOG":
                        catalog = ast.literal_eval(node.value)
                    elif target.id == "ALCO_DEPOTS":
                        depots = ast.literal_eval(node.value)
except Exception as e:
    print(f"[WARN] Could not parse catalog from api.py: {e}")

# Pre-compute dynamic gradients from packaging images
print("[ALCO SERVER] Pre-computing dynamic image gradients...")
for item in catalog:
    img = item.get("image_url")
    if img:
        try:
            grad, prim, sec, breakdown = extract_dynamic_gradient(img)
            item["gradient"] = grad
            item["theme_color"] = prim
            item["color_breakdown"] = breakdown
            print(f"  ✓ {item.get('item_name')}: {prim} -> {sec}")
        except Exception as e:
            print(f"  ✗ {item.get('item_name')}: {e}")
print("[ALCO SERVER] Image gradients pre-computed.")

# -------------------------------------------------------------
# 2. SEED ORDERS DB IF NOT PRESENT
# -------------------------------------------------------------
if not os.path.exists(ORDERS_FILE):
    initial_orders = [
        {
            "name": "ORD-2026-0001",
            "chemist_doctor_name": "Lazz Pharma (Dhanmondi)",
            "phone_number": "01711223344",
            "zone": "DK.B",
            "territory_region": "Dhaka South",
            "mpo_code": "D073",
            "field_agent_name": "Mr. Md. Masud Rana",
            "payment_method": "Cash",
            "grand_total": 3600.0,
            "vat_amount": 540.0,
            "due_amount": 0.0,
            "status": "Proceeded",
            "erpnext_sales_order": "SO-2026-0001",
            "creation": "2026-08-25 10:15:00",
            "order_date": "2026-08-25",
            "items": [{"item_code": "ALO-PAN-40", "item_name": "Pantopra 40", "qty": 20, "rate": 180.0, "amount": 3600.0}]
        },
        {
            "name": "ORD-2026-0002",
            "chemist_doctor_name": "Durlob Pharmacy",
            "phone_number": "01907430431",
            "zone": "FRD.A",
            "territory_region": "Faridpur Sadar",
            "mpo_code": "F055",
            "field_agent_name": "Kalam Mia",
            "payment_method": "Credit",
            "grand_total": 1200.0,
            "vat_amount": 180.0,
            "due_amount": 1200.0,
            "status": "Submitted",
            "erpnext_sales_order": None,
            "creation": "2026-08-25 11:30:00",
            "order_date": "2026-08-25",
            "items": [{"item_code": "ALO-CAL-500", "item_name": "Calmi 500", "qty": 15, "rate": 80.0, "amount": 1200.0}]
        }
    ]
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(initial_orders, f, indent=2)

def get_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)

# -------------------------------------------------------------
# 3. HTTP REQUEST HANDLER
# -------------------------------------------------------------
class AlcoRequestHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Static / Page routes
        if path in ["/", "/index", "/index.html"]:
            self.serve_file(os.path.join(WWW_DIR, "index.html"), "text/html")
        elif path in ["/alco-order", "/alco-order.html", "/alco_order", "/alco_order.html"]:
            self.serve_file(os.path.join(WWW_DIR, "alco-order.html"), "text/html")
        elif path in ["/alco-admin", "/alco-admin.html"]:
            self.serve_file(os.path.join(WWW_DIR, "alco-admin.html"), "text/html")
        elif path.startswith("/assets/alco_ecommerce/"):
            rel = path[len("/assets/alco_ecommerce/"):]
            full_path = os.path.join(PUBLIC_DIR, rel)
            self.serve_file(full_path)
        # API Routes
        elif path == "/api/method/alco_ecommerce.api.get_pharma_products" or path == "/api/method/alco_ecommerce.api.get_catalog":
            self.send_json({"message": catalog})
        elif path == "/api/method/alco_ecommerce.api.get_image_gradient":
            img_url = query.get("image_url", [None])[0] or query.get("url", [None])[0]
            if img_url:
                grad, prim, sec, breakdown = extract_dynamic_gradient(img_url)
                self.send_json({
                    "message": {
                        "gradient": grad,
                        "primary_color": prim,
                        "secondary_color": sec,
                        "color_breakdown": breakdown
                    }
                })
            else:
                self.send_json({"message": {"error": "Missing image_url parameter"}}, 400)
        elif path == "/api/method/alco_ecommerce.api.get_depots_list":
            self.send_json({"message": depots})
        elif path == "/api/method/alco_ecommerce.api.get_orders_list" or path == "/api/method/alco_ecommerce.api.get_field_orders":
            orders = get_orders()
            self.send_json({"message": orders})
        elif path == "/api/method/alco_ecommerce.api.get_dashboard_summary":
            orders = get_orders()
            total_rev = sum(o.get("grand_total", 0) for o in orders)
            total_vat = sum(o.get("vat_amount", 0) for o in orders)
            self.send_json({
                "message": {
                    "total_orders": len(orders),
                    "total_revenue": total_rev or 185420.0,
                    "total_vat": total_vat or 27813.0,
                    "total_chemists": 1000,
                    "total_field_forces": 787,
                    "total_depots": len(depots),
                    "recent_orders": orders[-10:][::-1],
                    "total_products": len(catalog)
                }
            })
        elif path == "/api/method/alco_ecommerce.api.get_customers_list":
            customers = [
                {"name": "Lazz Pharma (Dhanmondi)", "phone": "01711223344", "address": "Dhanmondi 32, Dhaka", "zone": "DK.B", "credit_limit": 50000.0, "due_balance": 12500.0, "status": "Active"},
                {"name": "Durlob Pharmacy", "phone": "01907430431", "address": "Faridpur Sadar", "zone": "FRD.A", "credit_limit": 30000.0, "due_balance": 4200.0, "status": "Active"},
                {"name": "Nipa Pharmacy", "phone": "01688065691", "address": "Mirpur-1, Dhaka", "zone": "DK.B", "credit_limit": 40000.0, "due_balance": 8900.0, "status": "Active"},
                {"name": "Bhai Bon Medical Hall", "phone": "01723543467", "address": "Mymensingh Town", "zone": "MYM.A", "credit_limit": 25000.0, "due_balance": 3100.0, "status": "Active"}
            ]
            self.send_json({"message": customers})
        elif path == "/api/method/alco_ecommerce.api.get_employees_list":
            employees = [
                {"emp_id": "EMP-001", "name": "Mr. Md. Masud Rana", "email": "masud.mpo@alcopharma.com", "designation": "MPO", "zone": "DK.B", "phone": "01711223301", "status": "Active"},
                {"emp_id": "EMP-002", "name": "Mr. Md. Parvez Hossain", "email": "parvez.mpo@alcopharma.com", "designation": "MPO", "zone": "DK.A", "phone": "01711223302", "status": "Active"},
                {"emp_id": "EMP-003", "name": "Golam Kibria", "email": "kibria.fm@alcopharma.com", "designation": "FM", "zone": "COM.A", "phone": "01711223303", "status": "Active"},
                {"emp_id": "EMP-004", "name": "AKM Zahirul Islam", "email": "zahirul.fm@alcopharma.com", "designation": "FM", "zone": "BARI.A", "phone": "01711223304", "status": "Active"}
            ]
            self.send_json({"message": employees})
        elif path == "/api/method/alco_ecommerce.api.get_operational_report":
            self.send_json({"message": [
                {"challan_no": "CH-2026-901", "invoice_no": "INV-ALC-881", "customer": "Lazz Pharma (Dhanmondi)", "zone": "DK.B", "depot": "Dhaka Metro Depot (DK-2)", "items_count": 5, "total_value": 24500.0, "status": "Dispatched", "vehicle_no": "DM-CHA-11-2041", "driver": "Md. Rafiq", "dispatch_time": "25 Aug 2026 10:30 AM"},
                {"challan_no": "CH-2026-902", "invoice_no": "INV-ALC-882", "customer": "Durlob Pharmacy", "zone": "FRD.A", "depot": "Faridpur Depot", "items_count": 3, "total_value": 14200.0, "status": "Delivered", "vehicle_no": "FRD-MA-04-1022", "driver": "Kalam Mia", "dispatch_time": "25 Aug 2026 09:15 AM"}
            ]})
        elif path == "/api/method/alco_ecommerce.api.get_sales_report":
            self.send_json({"message": [
                {"item_code": "ALO-PAN-40", "item_name": "Pantopra 40", "pack_size": "40 mg Tablet [42's]", "qty_sold": 18450, "bonus_qty": 1845, "rate": 180.0, "gross_sales": 3321000.0, "vat": 498150.0, "net_sales": 3819150.0},
                {"item_code": "ALO-CAL-500", "item_name": "Calmi 500", "pack_size": "500 mg Tablet [50's]", "qty_sold": 24200, "bonus_qty": 2420, "rate": 80.0, "gross_sales": 1936000.0, "vat": 290400.0, "net_sales": 2226400.0}
            ]})
        elif path == "/api/method/alco_ecommerce.api.get_monthly_sales_collection":
            self.send_json({"message": [
                {"month": "August 2026", "target": 16500000.0, "sales": 14200000.0, "collection": 13800000.0, "achievement_pct": "86.1% (MTD)", "collection_pct": "97.1%"}
            ]})
        elif path == "/api/method/alco_ecommerce.api.get_receivings_list":
            self.send_json({"message": [
                {"grn_no": "GRN-2026-0811", "date": "24 Aug 2026", "invoice": "PLANT-INV-7741", "supplier": "Alco Pharma Plant (Mirpur-7)", "depot": "Dhaka Central Depot (DK-1)", "items_count": 4, "amount_paid": 450000.0, "total_amount": 450000.0, "status": "Verified"}
            ]})
        elif path == "/api/method/alco_ecommerce.api.get_customer_sales_return":
            self.send_json({"message": [
                {"customer": "Lazz Pharma (Dhanmondi)", "zone": "DK.B", "gross_sales": 245000.0, "returns": 3200.0, "net_sales": 241800.0, "return_reason": "Near Expiry Batches (Replaced)"}
            ]})
        elif path == "/health":
            self.send_json({"status": "healthy", "service": "Alco Ecommerce", "port": 8080})
        else:
            self.send_error(404, f"File Not Found: {path}")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(length) if length > 0 else b"{}"

        try:
            body = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            body = {}

        if path == "/api/method/alco_ecommerce.api.submit_field_order":
            chemist = body.get("chemist_doctor_name") or "Direct Customer"
            phone = body.get("phone_number", "")
            zone = body.get("zone", "DK.B")
            payment = body.get("payment_method", "Cash")
            items = body.get("items_json", [])
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except Exception:
                    items = []

            orders = get_orders()
            new_id = f"ORD-2026-{len(orders) + 1:04d}"
            grand_total = sum(float(i.get("rate", 0)) * float(i.get("qty", 1)) for i in items)
            vat = round(grand_total * 0.15, 2)
            due = grand_total if payment in ["Credit", "bKash / Nagad"] else 0.0

            order_record = {
                "name": new_id,
                "chemist_doctor_name": chemist,
                "phone_number": phone,
                "zone": zone,
                "territory_region": body.get("territory_region", zone),
                "mpo_code": body.get("mpo_code", "D067"),
                "field_agent_name": body.get("field_agent_name", "Online Customer"),
                "payment_method": payment,
                "grand_total": grand_total,
                "vat_amount": vat,
                "due_amount": due,
                "status": "Submitted",
                "erpnext_sales_order": None,
                "creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "order_date": datetime.now().strftime("%Y-%m-%d"),
                "items": items
            }
            orders.append(order_record)
            save_orders(orders)

            self.send_json({
                "message": {
                    "success": True,
                    "docname": new_id,
                    "grand_total": grand_total,
                    "vat_amount": vat,
                    "due_amount": due,
                    "status": "Submitted"
                }
            })
        elif path == "/api/method/alco_ecommerce.api.create_erpnext_sales_order":
            order_name = body.get("field_order_name")
            orders = get_orders()
            found = False
            so_name = f"SO-2026-{datetime.now().strftime('%M%S')}"
            for o in orders:
                if o.get("name") == order_name:
                    o["status"] = "Proceeded"
                    o["erpnext_sales_order"] = so_name
                    found = True
                    break
            if found:
                save_orders(orders)
                self.send_json({
                    "message": {
                        "success": True,
                        "sales_order": so_name,
                        "message": f"ERPNext Sales Order {so_name} created and submitted successfully!"
                    }
                })
            else:
                self.send_json({"message": {"success": False, "message": "Order not found"}}, 404)
        elif path == "/api/method/alco_ecommerce.api.update_product_details":
            item_code = body.get("item_code")
            offer_price = float(body.get("offer_price", 0))
            stock_qty = float(body.get("stock_qty", 0))
            for p in catalog:
                if p.get("item_code") == item_code:
                    p["offer_price"] = offer_price
                    p["rate"] = offer_price
                    p["stock_qty"] = stock_qty
                    break
            self.send_json({"message": {"success": True, "message": f"Product {item_code} updated successfully!"}})
        elif path == "/api/method/alco_ecommerce.api.get_image_gradient":
            img_url = body.get("image_url") or body.get("url")
            if img_url:
                grad, prim, sec, breakdown = extract_dynamic_gradient(img_url)
                self.send_json({
                    "message": {
                        "gradient": grad,
                        "primary_color": prim,
                        "secondary_color": sec,
                        "color_breakdown": breakdown
                    }
                })
            else:
                self.send_json({"message": {"error": "Missing image_url parameter"}}, 400)
        else:
            self.send_error(404, f"API endpoint not found: {path}")

    def send_json(self, data, status=200):
        content = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(content)

    def serve_file(self, filepath, content_type=None):
        if not os.path.exists(filepath):
            self.send_error(404, f"File not found: {filepath}")
            return
        if not content_type:
            if filepath.endswith(".html"):
                content_type = "text/html; charset=utf-8"
            elif filepath.endswith(".svg"):
                content_type = "image/svg+xml"
            elif filepath.endswith(".png"):
                content_type = "image/png"
            elif filepath.endswith(".css"):
                content_type = "text/css; charset=utf-8"
            elif filepath.endswith(".js"):
                content_type = "application/javascript; charset=utf-8"
            else:
                content_type = "application/octet-stream"

        with open(filepath, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        if filepath.endswith((".png", ".jpg", ".jpeg", ".svg", ".woff2")):
            self.send_header("Cache-Control", "public, max-age=86400, immutable")
        else:
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(content)

class ThreadedAlcoServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run():
    port = 8080
    server_address = ("0.0.0.0", port)
    with ThreadedAlcoServer(server_address, AlcoRequestHandler) as httpd:
        print(f"[ALCO SERVER] Multi-threaded high-performance server running at http://0.0.0.0:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
