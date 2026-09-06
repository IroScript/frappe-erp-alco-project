import re

with open(r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Orders_Page.txt", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Extract the full <style> tag
style_match = re.search(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
styles = style_match.group(1) if style_match else ""

# 2. Extract the body HTML
body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
body_html = body_match.group(1) if body_match else ""

# Remove the original <script> tags at the end of body which refer to live nuxt bundles that won't load locally
body_clean = re.sub(r"<script.*?</script>", "", body_html, flags=re.DOTALL)

# Let's inspect the table and rows in body_clean
tbody_match = re.search(r"(<tbody[^>]*>)(.*?)(</tbody>)", body_clean, re.DOTALL)
if tbody_match:
    print("Found tbody!")
    # Get first row template
    row_match = re.search(r"(<tr[^>]*>.*?</tr>)", tbody_match.group(2), re.DOTALL)
    if row_match:
        print("Found row template length:", len(row_match.group(1)))
        print("Sample row:", row_match.group(1)[:400])

print("Total clean body length:", len(body_clean))
