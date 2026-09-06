import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd\HomePage.txt", "r", encoding="utf-8", errors="ignore") as f:
    fe_home = f.read()

# Let's find product cards structure
cards = re.findall(r"(<div class=\"product-card.*?</div>\s*</div>\s*</div>)", fe_home, re.DOTALL)
print("Found product cards in FrontEnd Home:", len(cards))
if cards:
    print("Sample card:\n", cards[0][:600])
