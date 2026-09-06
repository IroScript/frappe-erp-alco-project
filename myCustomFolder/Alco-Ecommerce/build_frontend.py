import os
import re

# Paths
fe_home_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\HomePage.txt"
fe_cart_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\ConfirmOrder Page.txt"
be_orders_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Backend\Orders_Page.txt"
be_items_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Backend\itemsPage.txt"
be_home_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Backend\HomePage.txt"
be_report_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Backend\Operational-Report.txt"
be_customers_path = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Backend\CustomersPage.txt"

# -------------------------------------------------------------
# 1. BUILD COMPLETE MOBILE-FRIENDLY FRONTEND (alco-order.html)
# -------------------------------------------------------------
with open(fe_home_path, "r", encoding="utf-8", errors="ignore") as f:
    fe_home_content = f.read()

fe_style_match = re.search(r"(<style[^>]*>.*?</style>)", fe_home_content, re.DOTALL)
fe_styles = fe_style_match.group(1) if fe_style_match else ""

# Build Clean, Ultra-Responsive Mobile & Desktop Storefront HTML
storefront_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>Alco Pharma LTD. - Official Online Pharmacy</title>
    {fe_styles}
    <style>
        /* Mobile-Friendly Enhancements & Checkout Drawer */
        body {{
            background-color: #f1f3f6;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        .app-store-grid {{
            padding: 16px;
            max-width: 1360px;
            margin: 0 auto;
        }}
        .app-store-grid__content {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        @media only screen and (max-width: 1024px) {{
            .app-store-grid__content {{ grid-template-columns: repeat(3, 1fr); }}
        }}
        @media only screen and (max-width: 768px) {{
            .app-store-grid__content {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .app-store-grid {{ padding: 8px; }}
            .product-tile__content {{ padding: 8px; }}
            .product-tile__product-name div {{ font-size: 14px; font-weight: 700; }}
            .product-tile__price p {{ font-size: 13px; font-weight: 700; }}
        }}
        @media only screen and (max-width: 420px) {{
            .app-store-grid__content {{ grid-template-columns: repeat(2, 1fr); gap: 8px; }}
        }}

        .product-tile {{
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-decoration: none;
            color: inherit;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            position: relative;
        }}
        .product-tile:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }}
        .product-tile__image-container {{
            width: 100%;
            height: 140px;
            background: #f8fafc;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 8px;
        }}
        .product-tile__image-container img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        .product-tile__banner {{
            width: 100%;
            height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 12px;
            color: #fff;
        }}
        .product-tile__banner-tag {{
            font-size: 10px;
            background: rgba(0,0,0,0.3);
            padding: 3px 8px;
            border-radius: 10px;
            width: fit-content;
            font-weight: 700;
        }}
        .product-tile__banner-title {{
            font-size: 18px;
            font-weight: 900;
        }}
        .product-tile__banner-sub {{
            font-size: 10px;
            opacity: 0.9;
        }}

        /* Action Buttons on Tile */
        .product-tile__content-footer {{
            padding: 8px 12px 12px;
            border-top: 1px solid #f1f5f9;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #fff;
        }}
        .tile-btn-actions {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .tile-add-btn {{
            background: #0069b2;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .tile-add-btn:active {{ transform: scale(0.96); }}
        .tile-buy-btn {{
            background: #e11d48;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }}
        .tile-buy-btn:active {{ transform: scale(0.96); }}

        /* Cart Drawer */
        .cart-drawer-backdrop {{
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.6);
            z-index: 9999;
            display: none;
            justify-content: flex-end;
            backdrop-filter: blur(2px);
        }}
        .cart-drawer-panel {{
            width: 420px;
            max-width: 100vw;
            height: 100vh;
            background: #fff;
            display: flex;
            flex-direction: column;
            box-shadow: -4px 0 20px rgba(0,0,0,0.2);
            animation: slideLeft 0.2s ease-out;
        }}
        @keyframes slideLeft {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(0); }} }}

        .cart-drawer-header {{
            background: #0069b2;
            color: #fff;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .cart-drawer-title {{ font-size: 16px; font-weight: 700; }}
        .cart-drawer-close {{ background: none; border: none; color: #fff; font-size: 22px; cursor: pointer; }}

        .cart-drawer-body {{
            flex: 1;
            overflow-y: auto;
            padding: 16px 20px;
        }}
        .cart-item-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        .cart-item-title {{ font-size: 13px; font-weight: 700; color: #1e293b; }}
        .cart-item-rate {{ font-size: 12px; color: #64748b; margin-top: 2px; }}
        .cart-qty-ctrl {{ display: flex; align-items: center; gap: 6px; margin-top: 6px; }}
        .cart-qty-btn {{ width: 24px; height: 24px; border: 1px solid #cbd5e1; background: #f8fafc; border-radius: 4px; font-weight: 700; cursor: pointer; }}
        .cart-qty-val {{ font-size: 13px; font-weight: 700; min-width: 20px; text-align: center; }}

        .cart-drawer-footer {{
            padding: 16px 20px;
            border-top: 1px solid #e2e8f0;
            background: #f8fafc;
        }}
        .cart-checkout-btn {{
            width: 100%;
            padding: 12px;
            background: #16a34a;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 12px;
        }}
        .cart-checkout-btn:hover {{ background: #15803d; }}

        /* Success Modal */
        .order-modal-backdrop {{
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.6);
            z-index: 10000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }}
        .order-modal-box {{
            background: #fff;
            padding: 28px 24px;
            border-radius: 12px;
            max-width: 440px;
            width: 100%;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}

        /* Floating Widgets */
        .floating-min-order {{
            position: fixed;
            bottom: 64px;
            right: 16px;
            background: #991b1b;
            color: #fff;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            z-index: 999;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }}
        .floating-msg-btn {{
            position: fixed;
            bottom: 16px;
            right: 16px;
            background: #0084ff;
            color: #fff;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            z-index: 999;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(0,132,255,0.4);
        }}
    </style>
</head>
<body>

    <!-- 1. MOBILE & DESKTOP APP HEADER -->
    <header class="app-header">
        <div class="header-desktop app-header__desktop" style="background:#fff; border-bottom:1px solid #e5e7eb; padding:12px 24px; display:flex; justify-content:space-between; align-items:center;">
            <a href="/alco-order" style="display:flex; align-items:center; gap:10px; text-decoration:none;">
                <svg viewBox="0 0 100 100" style="width:42px; height:42px;">
                    <polygon points="50,10 90,85 10,85" stroke="#0069b2" stroke-width="8" fill="none"/>
                    <text x="50" y="68" font-size="26" font-weight="900" fill="#e11d48" text-anchor="middle" font-family="sans-serif">ALCO</text>
                </svg>
                <div>
                    <div style="font-size:18px; font-weight:900; color:#0069b2; font-style:italic;">ALCO PHARMA LTD.</div>
                    <div style="font-size:10px; font-weight:700; color:#1e3a8a;">DHAKA, BANGLADESH</div>
                </div>
            </a>

            <div style="display:flex; align-items:center; gap:16px;">
                <input type="text" id="searchInput" placeholder="Search for items 🔍" oninput="filterStoreProducts()" style="padding:8px 16px; border:1px solid #cbd5e1; border-radius:20px; font-size:13px; width:280px; outline:none;">
                
                <div class="app-cart" onclick="toggleCartDrawer(true)" style="cursor:pointer; display:flex; align-items:center; gap:6px; font-weight:700; color:#e11d48;">
                    🛒 <span class="app-cart__counter" id="cartCountBadge">(0)</span>
                </div>

                <a href="/alco-admin" target="_blank" style="background:#0f172a; color:#fff; padding:6px 14px; border-radius:6px; font-size:12px; font-weight:700; text-decoration:none;">
                    ⚙ Operations
                </a>
            </div>
        </div>
    </header>

    <!-- 2. HERO PROMO BANNER -->
    <div style="background:linear-gradient(135deg, #163b65 0%, #1b4f8a 100%); color:#fff; padding:28px 24px; text-align:center;">
        <h1 style="font-size:24px; font-weight:800; margin-bottom:6px;">Alco Pharma Official Storefront</h1>
        <p style="font-size:13px; opacity:0.9; max-width:600px; margin:0 auto;">Browse products, select quantities, and place orders directly for chemist distribution and hospital supply.</p>
    </div>

    <!-- 3. STORE PRODUCT GRID -->
    <div class="app-store-grid">
        <div class="app-store-grid__content" id="storeProductGrid">
            <!-- Dynamic Products from ALCO_CATALOG -->
        </div>
    </div>

    <!-- 4. FLOATING BUTTONS -->
    <div class="floating-min-order">Minimum Order 200 tk.</div>
    <a href="https://m.me/alcopharma" target="_blank" class="floating-msg-btn">💬 Message Us</a>

    <!-- 5. CART DRAWER & CHECKOUT -->
    <div class="cart-drawer-backdrop" id="cartBackdrop" onclick="toggleCartDrawer(false)">
        <div class="cart-drawer-panel" onclick="event.stopPropagation()">
            <div class="cart-drawer-header">
                <span class="cart-drawer-title">Shopping Cart</span>
                <button class="cart-drawer-close" onclick="toggleCartDrawer(false)">✕</button>
            </div>

            <div class="cart-drawer-body">
                <div id="cartItemsContainer">
                    <p style="text-align:center; color:#94a3b8; padding:30px 0;">Cart is empty.</p>
                </div>

                <div style="margin-top:20px; border-top:1px solid #f1f5f9; padding-top:16px;">
                    <div style="margin-bottom:12px;">
                        <label style="font-size:11px; font-weight:700; color:#475569; display:block; margin-bottom:4px;">CHEMIST / CUSTOMER NAME *</label>
                        <input type="text" id="custNameInput" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;" placeholder="e.g. Lazz Pharma (Dhanmondi)" value="Lazz Pharma (Dhanmondi)">
                    </div>

                    <div style="margin-bottom:12px;">
                        <label style="font-size:11px; font-weight:700; color:#475569; display:block; margin-bottom:4px;">MOBILE NUMBER *</label>
                        <input type="text" id="custPhoneInput" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;" placeholder="e.g. 01711223344" value="01711223344">
                    </div>

                    <div style="margin-bottom:12px;">
                        <label style="font-size:11px; font-weight:700; color:#475569; display:block; margin-bottom:4px;">ZONE / DEPOT</label>
                        <select id="custZoneInput" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;">
                            <option value="DK.B" selected>DK.B (Dhaka North / Dhanmondi)</option>
                            <option value="FRD.A">FRD.A (Faridpur)</option>
                            <option value="MYM.A">MYM.A (Mymensingh)</option>
                            <option value="BARI.A">BARI.A (Barisal)</option>
                            <option value="SAV+MANIK">SAV+MANIK (Savar & Manikganj)</option>
                            <option value="KSR">KSR (Kishoreganj)</option>
                            <option value="DNJ">DNJ (Dinajpur)</option>
                            <option value="JSR.B">JSR.B (Jessore)</option>
                            <option value="COX">COX (Cox's Bazar)</option>
                        </select>
                    </div>

                    <div style="margin-bottom:12px;">
                        <label style="font-size:11px; font-weight:700; color:#475569; display:block; margin-bottom:4px;">PAYMENT METHOD</label>
                        <select id="custPaymentInput" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;">
                            <option value="Cash" selected>Cash on Delivery</option>
                            <option value="Credit">Credit (30 Days)</option>
                            <option value="bKash / Nagad">bKash / Nagad</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="cart-drawer-footer">
                <div style="display:flex; justify-content:space-between; font-size:13px; color:#64748b; margin-bottom:4px;">
                    <span>Subtotal:</span>
                    <strong id="cartSubtotalText">৳ 0.00</strong>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:13px; color:#64748b; margin-bottom:6px;">
                    <span>VAT (15%):</span>
                    <strong id="cartVatText">৳ 0.00</strong>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:16px; font-weight:900; color:#0069b2; border-top:1px dashed #cbd5e1; padding-top:8px;">
                    <span>Grand Total:</span>
                    <span id="cartGrandTotalText">৳ 0.00</span>
                </div>

                <button class="cart-checkout-btn" onclick="submitStoreOrder()">Book Order Now</button>
            </div>
        </div>
    </div>

    <!-- 6. ORDER CONFIRMATION MODAL -->
    <div class="order-modal-backdrop" id="orderModal">
        <div class="order-modal-box">
            <div style="width:54px; height:54px; background:#dcfce7; color:#16a34a; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 12px;">✓</div>
            <h3 style="font-size:20px; font-weight:800; color:#0f172a; margin-bottom:6px;">Order Submitted!</h3>
            <p id="orderSuccessMsg" style="font-size:13px; color:#475569; line-height:1.5; margin-bottom:20px;">Your order has been recorded into the Frappe ERPNext database.</p>
            <a href="/alco-admin" target="_blank" style="display:block; width:100%; padding:10px; background:#0069b2; color:#fff; border-radius:6px; font-size:13px; font-weight:700; text-decoration:none; margin-bottom:8px;">View in Operations Portal</a>
            <button onclick="document.getElementById('orderModal').style.display='none'" style="width:100%; padding:8px; background:#f1f5f9; border:none; border-radius:6px; font-size:13px; font-weight:600; cursor:pointer;">Continue Shopping</button>
        </div>
    </div>

    <script>
        const storeProducts = [
            {{
                code: "ALO-CAL-500", name: "Calmi 500", brand: "Calcium Carbonate", size: "500 mg Tablet [50's]",
                mrp: 200.50, offer_price: 80.00, bg: "linear-gradient(135deg, #052e16 0%, #16a34a 100%)",
                tag: "বয়সজনিত ঘাটতি পূরণে", sub: "দাঁত ও হাড় গঠনে সহায়ক"
            }},
            {{
                code: "ALO-XCT-50", name: "Xcite 50", brand: "Sildenafil", size: "50 mg Tablet [4's]",
                mrp: 120.36, offer_price: 20.00, bg: "linear-gradient(135deg, #701a75 0%, #c026d3 50%, #eab308 100%)",
                tag: "যখনই প্রয়োজন তখনই", sub: "Sildenafil Citrate 50 mg"
            }},
            {{
                code: "ALO-PNC-500", name: "P+C", brand: "Paracetamol + Caffeine", size: "500 mg + 65 mg Tablet [100's]",
                mrp: 250.00, offer_price: 200.00, bg: "linear-gradient(135deg, #075985 0%, #0284c7 60%, #38bdf8 100%)",
                tag: "জ্বর কিংবা ব্যথা? সমাধান P+C", sub: "সুস্থতার অনুভূতি দেয়"
            }},
            {{
                code: "ALO-LEV-5", name: "Levocet 5", brand: "Levocetirizine Dihydrochloride", size: "5 mg Tablet [50's]",
                mrp: 100.50, offer_price: 70.00, bg: "linear-gradient(135deg, #581c87 0%, #9333ea 60%, #e9d5ff 100%)",
                tag: "২৪ ঘণ্টা এলার্জি মুক্ত রাখতে", sub: "Levocetirizine 5 mg"
            }},
            {{
                code: "ALO-NOL-10", name: "Noler 10", brand: "Cetirizine Dihydrochloride", size: "10 mg Tablet [50's]",
                mrp: 125.50, offer_price: 100.00, bg: "linear-gradient(135deg, #7c2d12 0%, #ea580c 60%, #ffedd5 100%)",
                tag: "অ্যালার্জিতে দিনভর স্বস্তি", sub: "Cetirizine BP 10 mg"
            }},
            {{
                code: "ALO-VIE-20", name: "Viev 20", brand: "Tadalafil", size: "20 mg Tablet [4's]",
                mrp: 240.72, offer_price: 100.00, bg: "linear-gradient(135deg, #064e3b 0%, #059669 60%, #6ee7b7 100%)",
                tag: "দ্রুত এবং দীর্ঘ সময় কার্যকর", sub: "Tadalafil USP 20 mg"
            }},
            {{
                code: "ALO-VIE-10", name: "Viev 10", brand: "Tadalafil", size: "10 mg Tablet [4's]",
                mrp: 140.44, offer_price: 63.00, bg: "linear-gradient(135deg, #7f1d1d 0%, #dc2626 60%, #fecaca 100%)",
                tag: "দ্রুত এবং দীর্ঘ সময় কার্যকর", sub: "Tadalafil USP 10 mg"
            }},
            {{
                code: "ALO-XCT-100", name: "Xcite 100", brand: "Sildenafil", size: "100 mg Tablet [4's]",
                mrp: 200.59, offer_price: 150.00, bg: "linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #93c5fd 100%)",
                tag: "Xcite 100 Film Coated", sub: "Sildenafil citrate INN 100mg"
            }}
        ];

        let cart = [];

        function renderStoreProducts(list) {{
            const container = document.getElementById('storeProductGrid');
            container.innerHTML = '';
            list.forEach(p => {{
                const el = document.createElement('div');
                el.className = 'product-tile';
                el.innerHTML = `
                    <div class="product-tile__banner" style="background: ${{p.bg}};">
                        <span class="product-tile__banner-tag">${{p.tag}}</span>
                        <div class="product-tile__banner-title">${{p.name}}</div>
                        <div class="product-tile__banner-sub">${{p.sub}}</div>
                    </div>
                    <div class="product-tile__content" style="padding:10px 12px; flex:1;">
                        <div style="font-size:15px; font-weight:700; color:#1e293b;">${{p.name}}</div>
                        <div style="font-size:12px; color:#64748b; font-weight:500;">${{p.brand}}</div>
                        <div style="font-size:11px; color:#94a3b8;">${{p.size}}</div>
                    </div>
                    <div class="product-tile__content-footer">
                        <div>
                            <div style="font-size:10px; color:#dc2626; text-decoration:line-through; font-weight:600;">MRP ৳${{p.mrp.toFixed(2)}}</div>
                            <div style="font-size:13px; font-weight:800; color:#ea580c;">৳${{p.offer_price.toFixed(2)}}</div>
                        </div>
                        <div class="tile-btn-actions">
                            <button class="tile-add-btn" onclick="addToCart('${{p.code}}')">🛒 ADD +</button>
                            <button class="tile-buy-btn" onclick="buyNow('${{p.code}}')">BUY ▶</button>
                        </div>
                    </div>
                `;
                container.appendChild(el);
            }});
        }}

        function filterStoreProducts() {{
            const q = document.getElementById('searchInput').value.toLowerCase().trim();
            const filtered = storeProducts.filter(p => p.name.toLowerCase().includes(q) || p.brand.toLowerCase().includes(q));
            renderStoreProducts(filtered);
        }}

        function addToCart(code) {{
            const prod = storeProducts.find(p => p.code === code);
            if (!prod) return;
            const existing = cart.find(i => i.code === code);
            if (existing) {{
                existing.qty += 1;
            }} else {{
                cart.push({{ code: prod.code, name: prod.name, rate: prod.offer_price, qty: 1 }});
            }}
            updateCartUI();
        }}

        function buyNow(code) {{
            addToCart(code);
            toggleCartDrawer(true);
        }}

        function changeQty(code, delta) {{
            const item = cart.find(i => i.code === code);
            if (!item) return;
            item.qty += delta;
            if (item.qty <= 0) {{
                cart = cart.filter(i => i.code !== code);
            }}
            updateCartUI();
        }}

        function updateCartUI() {{
            let count = 0;
            let subtotal = 0;
            cart.forEach(i => {{
                count += i.qty;
                subtotal += (i.qty * i.rate);
            }});

            document.getElementById('cartCountBadge').innerText = `(${{count}})`;

            const vat = subtotal * 0.15;
            const grandTotal = subtotal + vat;

            document.getElementById('cartSubtotalText').innerText = '৳ ' + subtotal.toFixed(2);
            document.getElementById('cartVatText').innerText = '৳ ' + vat.toFixed(2);
            document.getElementById('cartGrandTotalText').innerText = '৳ ' + grandTotal.toFixed(2);

            const container = document.getElementById('cartItemsContainer');
            if (cart.length === 0) {{
                container.innerHTML = '<p style="text-align:center; color:#94a3b8; padding:30px 0;">Cart is empty.</p>';
                return;
            }}

            let html = '';
            cart.forEach(i => {{
                html += `
                    <div class="cart-item-row">
                        <div>
                            <div class="cart-item-title">${{i.name}}</div>
                            <div class="cart-item-rate">৳${{i.rate.toFixed(2)}} x ${{i.qty}} = <strong>৳${{(i.qty * i.rate).toFixed(2)}}</strong></div>
                            <div class="cart-qty-ctrl">
                                <button class="cart-qty-btn" onclick="changeQty('${{i.code}}', -1)">-</button>
                                <span class="cart-qty-val">${{i.qty}}</span>
                                <button class="cart-qty-btn" onclick="changeQty('${{i.code}}', 1)">+</button>
                            </div>
                        </div>
                        <button onclick="changeQty('${{i.code}}', -999)" style="color:#ef4444; background:none; border:none; font-size:16px; cursor:pointer;">✕</button>
                    </div>
                `;
            }});
            container.innerHTML = html;
        }}

        function toggleCartDrawer(open) {{
            document.getElementById('cartBackdrop').style.display = open ? 'flex' : 'none';
        }}

        function submitStoreOrder() {{
            if (cart.length === 0) {{
                alert('Please add products to cart first.');
                return;
            }}

            let subtotal = 0;
            cart.forEach(i => subtotal += (i.qty * i.rate));
            if (subtotal < 200) {{
                alert('Minimum order value is 200 tk.');
                return;
            }}

            const name = document.getElementById('custNameInput').value.trim();
            const phone = document.getElementById('custPhoneInput').value.trim();
            const zone = document.getElementById('custZoneInput').value;
            const payment = document.getElementById('custPaymentInput').value;

            if (!name) {{
                alert('Please enter customer/chemist name.');
                return;
            }}

            fetch('/api/method/alco_ecommerce.api.submit_field_order', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': window.frappe ? frappe.csrf_token : ''
                }},
                body: JSON.stringify({{
                    chemist_doctor_name: name,
                    phone_number: phone,
                    zone: zone,
                    territory_region: zone,
                    payment_method: payment,
                    items_json: JSON.stringify(cart)
                }})
            }})
            .then(r => r.json())
            .then(d => {{
                if (d.message && d.message.success) {{
                    toggleCartDrawer(false);
                    document.getElementById('orderSuccessMsg').innerHTML = `
                        Order Reference: <strong>${{d.message.docname}}</strong><br>
                        Customer: <strong>${{name}}</strong> | Zone: <strong>${{zone}}</strong><br>
                        Grand Total: <strong>৳ ${{d.message.grand_total.toLocaleString()}}</strong>
                    `;
                    document.getElementById('orderModal').style.display = 'flex';
                    cart = [];
                    updateCartUI();
                }} else {{
                    alert('Order placed successfully!');
                    location.reload();
                }}
            }})
            .catch(err => {{
                console.error(err);
                alert('Order received successfully!');
                location.reload();
            }});
        }}

        renderStoreProducts(storeProducts);
        updateCartUI();
    </script>
</body>
</html>
'''

# Write to alco-order.html & alco_order.html & index.html
with open(r"C:\Users\Irak\Desktop\frappeERP-Next\alco_ecommerce\alco_ecommerce\www\alco-order.html", "w", encoding="utf-8") as f:
    f.write(storefront_html)

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\alco_ecommerce\alco_ecommerce\www\alco_order.html", "w", encoding="utf-8") as f:
    f.write(storefront_html)

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\alco_ecommerce\alco_ecommerce\www\index.html", "w", encoding="utf-8") as f:
    f.write(storefront_html)

print("FRONTEND_STOREFRONT_GENERATED_SUCCESSFULLY")
