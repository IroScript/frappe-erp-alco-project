import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\HomePage.txt", "r", encoding="utf-8", errors="ignore") as f:
    fe_home = f.read()

classes = set(re.findall(r'class="([^"]+)"', fe_home))
print("Frontend Classes sample:", sorted(list(classes))[:40])
