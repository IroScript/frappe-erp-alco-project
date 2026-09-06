import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\HomePage.txt", "r", encoding="utf-8", errors="ignore") as f:
    fe_home = f.read()

# Extract <style> block
style_match = re.search(r"(<style[^>]*>.*?</style>)", fe_home, re.DOTALL)
fe_styles = style_match.group(1) if style_match else ""
print("Frontend Styles length:", len(fe_styles))

# Extract body
body_match = re.search(r"<body[^>]*>(.*?)</body>", fe_home, re.DOTALL)
fe_body = body_match.group(1) if body_match else ""
fe_clean_body = re.sub(r"<script.*?</script>", "", fe_body, flags=re.DOTALL)
print("Frontend clean body length:", len(fe_clean_body))
