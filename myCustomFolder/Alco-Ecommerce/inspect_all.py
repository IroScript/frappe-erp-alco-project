import os
import re

frontend_dir = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\FrontEnd"
backend_dir = r"C:\Users\Irak\Desktop\frappeERP-Next\myCustomFolder\Alco-Ecommerce\SourceCodes\Backend"

print("--- FRONTEND FILES ---")
for f in os.listdir(frontend_dir):
    p = os.path.join(frontend_dir, f)
    with open(p, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    title = re.search(r"<title>(.*?)</title>", content)
    print(f"File: {f} | Size: {len(content)} | Styles count: {len(styles)} | Title: {title.group(1) if title else 'N/A'}")

print("\n--- BACKEND FILES ---")
for f in os.listdir(backend_dir):
    p = os.path.join(backend_dir, f)
    with open(p, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    title = re.search(r"<title>(.*?)</title>", content)
    print(f"File: {f} | Size: {len(content)} | Styles count: {len(styles)} | Title: {title.group(1) if title else 'N/A'}")
