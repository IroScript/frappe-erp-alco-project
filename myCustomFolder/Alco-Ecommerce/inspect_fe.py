import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\HomePage.txt", "r", encoding="utf-8", errors="ignore") as f:
    fe_home = f.read()

body_match = re.search(r"<body[^>]*>(.*?)</body>", fe_home, re.DOTALL)
if body_match:
    body = body_match.group(1)
    body_clean = re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL)
    print("FrontEnd Home clean body length:", len(body_clean))
    print("Sample snippet:\n", body_clean[:800])
