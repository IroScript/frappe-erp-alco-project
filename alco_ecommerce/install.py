"""Install-time wiring of alco_ecommerce to core ERPNext masters (Frappe/ERPNext v16+).

Everything here goes through core DocTypes and the document API (no DDL, no core edits):
  * Price List "MRP" (selling, company currency) next to ERPNext's "Standard Selling"
  * Alco product catalog -> ERPNext Item (+ Item Barcode, opening stock via Item.opening_stock -> Stock Entry)
  * Item Price rows (MRP / Standard Selling, UOM Box) used by api.get_pharma_products and
    AlcoFieldOrder.validate_and_sync_items

All functions are idempotent: existing records are never overwritten (prices edited later in ERPNext stay intact).

Local docs used:
  frappe-docs-latest/framework/user/en/python-api/hooks.md            (Install Hooks: after_install)
  frappe-docs-latest/framework/user/en/api/document.md                (frappe.get_doc / insert)
  frappe-docs-latest/framework/user/en/api/database.md                (frappe.db.exists / get_value)
  frappe-docs-latest/erpnext/item-price.md, erpnext/price-lists.md    (Item Price / Price List semantics)

Manual run (e.g. after the ERPNext setup wizard on an existing site):
  bench --site <site> execute alco_ecommerce.install.setup_alco_masters
"""

import frappe
from frappe import _

PRICE_LISTS = ("MRP", "Standard Selling")
BOX_UOM = "Box"


def after_install() -> None:
	"""Hook: runs once when the app is installed on a site."""
	if not frappe.is_setup_complete():
		# Company / warehouses / currency do not exist before the ERPNext setup wizard.
		print("alco_ecommerce: ERPNext setup wizard not completed; run "
			  "`bench --site <site> execute alco_ecommerce.install.setup_alco_masters` afterwards.")
		return
	setup_alco_masters()


def setup_alco_masters() -> dict:
	"""Create the ERPNext master records the storefront/admin portal relies on (idempotent)."""
	if not frappe.is_setup_complete():
		frappe.throw(_("Complete the ERPNext setup wizard first (Company, currency, warehouses)."))
	currency = _company_currency()
	ensure_price_lists(currency)
	created = seed_catalog(currency)
	frappe.db.commit()  # module-level setup function (not a document hook)
	return {"currency": currency, **created}


def _company_currency() -> str:
	company = frappe.defaults.get_global_default("company") or frappe.db.get_value("Company", {}, "name")
	if not company:
		frappe.throw(_("No Company found. Complete the ERPNext setup wizard first."))
	return frappe.get_cached_value("Company", company, "default_currency")


def ensure_price_lists(currency: str) -> None:
	for name in PRICE_LISTS:
		if not frappe.db.exists("Price List", name):
			frappe.get_doc({
				"doctype": "Price List",
				"price_list_name": name,
				"currency": currency,
				"selling": 1,
				"enabled": 1,
			}).insert(ignore_permissions=True)


def _item_group() -> str:
	if frappe.db.exists("Item Group", "Products"):
		return "Products"
	return frappe.db.get_value("Item Group", {"is_group": 0}, "name")


def seed_catalog(currency: str) -> dict:
	"""Create missing Items + Item Prices from the app's canonical catalog (api.ALCO_CATALOG)."""
	from alco_ecommerce.api import ALCO_CATALOG

	items_created, prices_created = 0, 0
	item_group = _item_group()
	for row in ALCO_CATALOG:
		code = row["item_code"]
		if not frappe.db.exists("Item", code):
			item = frappe.get_doc({
				"doctype": "Item",
				"item_code": code,
				"item_name": row["item_name"],
				"item_group": item_group,
				"stock_uom": BOX_UOM,
				"is_stock_item": 1,
				"is_sales_item": 1,
				"include_item_in_manufacturing": 0,
				"description": row.get("description") or row["item_name"],
				"image": row.get("image_url"),
				"valuation_rate": row.get("cost") or 0,
				"opening_stock": row.get("stock_qty") or 0,  # core Item.set_opening_stock -> Stock Entry
				"custom_generic_name": row.get("generic_name"),
				"custom_pack_size": row.get("pack_size"),
				"custom_vat_percentage": row.get("vat_percentage") or 15,
				"custom_theme_color": row.get("theme_color"),
				"custom_gradient": row.get("gradient"),
				"custom_banner_tag": row.get("banner_tag"),
				"custom_banner_sub": row.get("banner_sub"),
				"barcodes": [{"barcode": row["upc"]}] if row.get("upc") else [],
			})
			item.insert(ignore_permissions=True)
			items_created += 1

		for price_list, rate in (("MRP", row.get("mrp")), ("Standard Selling", row.get("rate"))):
			if rate is None:
				continue
			exists = frappe.db.exists("Item Price", {
				"item_code": code, "price_list": price_list, "uom": BOX_UOM, "currency": currency,
			})
			if not exists:
				frappe.get_doc({
					"doctype": "Item Price",
					"item_code": code,
					"price_list": price_list,
					"uom": BOX_UOM,
					"currency": currency,
					"price_list_rate": rate,
				}).insert(ignore_permissions=True)
				prices_created += 1
	return {"items_created": items_created, "prices_created": prices_created}
