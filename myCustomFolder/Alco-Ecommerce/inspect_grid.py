import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\HomePage.txt", "r", encoding="utf-8", errors="ignore") as f:
    fe_home = f.read()

grid_match = re.search(r"(<div class=\"app-store-grid.*?)(<footer.*?</footer>)", fe_home, re.DOTALL)
if grid_match:
    print("Found grid match, length:", len(grid_match.group(1)))
    print("Sample grid markup:\n", grid_match.group(1)[:1200])
