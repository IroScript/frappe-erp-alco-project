import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\ConfirmOrder Page.txt", "r", encoding="utf-8", errors="ignore") as f:
    fe_cart = f.read()

body_match = re.search(r"<body[^>]*>(.*?)</body>", fe_cart, re.DOTALL)
if body_match:
    body = body_match.group(1)
    body_clean = re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL)
    print("Cart / Confirm Order clean body length:", len(body_clean))
    print("Sample snippet:\n", body_clean[:800])
