import re
import frappe
from frappe import _
from frappe.model.document import Document

class AlcoFieldOrder(Document):
    """
    Frappe v16 Controller for Alco Field Order.
    Foundation for Order Management & Checkout:
    - Chemist & Customer validation (BD phone, non-empty name, zone)
    - Line item validation & authoritative rate synchronization from tabItem Price
    - Positive whole-number box quantity enforcement
    - Authoritative 15% VAT and totals recalculation
    - Idempotency key uniqueness check
    """

    VALID_ZONES = {
        "DK.A", "DK.B", "CTG.A", "COM.A", "BARI.A",
        "FRD.A", "JSR.A", "MYM.A", "RAJ.A", "RNG.A", "SYL.A",
        "Dhaka North", "Dhaka South", "Chittagong South", "Sylhet Central",
        "Rajshahi West", "Khulna Region"
    }

    VALID_PAYMENTS = {"Cash", "Credit", "Bank Transfer", "bKash / Nagad"}

    def validate(self):
        """v16 Document validation lifecycle for Alco Field Orders"""
        self.validate_customer_info()
        self.validate_and_sync_items()
        self.recalculate_totals()
        self.validate_idempotency()

    def validate_customer_info(self):
        if not self.chemist_doctor_name or not str(self.chemist_doctor_name).strip():
            frappe.throw(_("Chemist / Doctor / Customer name is required."), title=_("Validation Error"))
        
        self.chemist_doctor_name = str(self.chemist_doctor_name).strip()
        if len(self.chemist_doctor_name) < 2:
            frappe.throw(_("Chemist / Doctor name must be at least 2 characters long."), title=_("Validation Error"))

        if self.phone_number:
            raw_phone = str(self.phone_number).strip()
            digits = re.sub(r"[^\d]", "", raw_phone)
            # Standard Bangladesh mobile: 11 digits starting with 01, or 13 digits starting with 8801
            if len(digits) == 13 and digits.startswith("8801"):
                digits = digits[2:]
            if len(digits) == 11 and digits.startswith("01"):
                self.phone_number = digits
            else:
                frappe.throw(
                    _("Invalid phone number: '{0}'. Must be a valid 11-digit Bangladeshi mobile number (e.g., 01711223344).").format(raw_phone),
                    title=_("Validation Error")
                )

        if self.payment_method and self.payment_method not in self.VALID_PAYMENTS:
            frappe.throw(
                _("Invalid payment method: '{0}'. Allowed methods: {1}").format(
                    self.payment_method, ", ".join(sorted(self.VALID_PAYMENTS))
                ),
                title=_("Validation Error")
            )

    def validate_and_sync_items(self):
        if not self.items or len(self.items) == 0:
            frappe.throw(_("Order must contain at least one product item."), title=_("Empty Order"))

        item_doctype = frappe.qb.DocType("Item")
        item_price_doctype = frappe.qb.DocType("Item Price")

        for idx, row in enumerate(self.items, start=1):
            if not row.item_code:
                frappe.throw(_("Row #{0}: Item code is required.").format(idx), title=_("Validation Error"))

            # Verify Item exists and is enabled
            item_data = (
                frappe.qb.from_(item_doctype)
                .select(item_doctype.item_name, item_doctype.disabled, item_doctype.is_sales_item)
                .where(item_doctype.name == row.item_code)
                .run(as_dict=True)
            )
            if not item_data:
                frappe.throw(_("Row #{0}: Item '{1}' does not exist in master catalog.").format(idx, row.item_code), title=_("Item Not Found"))
            
            item_record = item_data[0]
            if item_record.get("disabled") == 1 or item_record.get("is_sales_item") == 0:
                frappe.throw(_("Row #{0}: Item '{1}' is disabled or not available for sales.").format(idx, row.item_code), title=_("Item Disabled"))

            if not row.item_name:
                row.item_name = item_record.get("item_name") or row.item_code

            # Quantity validation: must be positive whole number of boxes
            qty = float(row.qty or 0)
            if qty <= 0:
                frappe.throw(_("Row #{0} ({1}): Quantity must be greater than zero.").format(idx, row.item_code), title=_("Invalid Quantity"))
            if not qty.is_integer():
                frappe.throw(_("Row #{0} ({1}): Quantity must be a whole number of boxes (got {2}).").format(idx, row.item_code, qty), title=_("Invalid Quantity"))
            
            row.qty = int(qty)
            row.uom = "Box"

            # Authoritative pricing lookup from tabItem Price (Single Source of Truth)
            price_data = (
                frappe.qb.from_(item_price_doctype)
                .select(item_price_doctype.price_list_rate)
                .where(
                    (item_price_doctype.item_code == row.item_code)
                    & (item_price_doctype.price_list == "Standard Selling")
                    & (item_price_doctype.uom == "Box")
                )
                .limit(1)
                .run(as_dict=True)
            )

            if price_data and price_data[0].get("price_list_rate") is not None:
                authoritative_rate = float(price_data[0].get("price_list_rate"))
                row.rate = authoritative_rate
            elif row.rate and float(row.rate) > 0:
                row.rate = float(row.rate)
            else:
                frappe.throw(
                    _("Row #{0}: No active selling price found for item '{1}' in Box UOM.").format(idx, row.item_code),
                    title=_("Price Missing")
                )

            row.amount = round(row.qty * row.rate, 2)

    def recalculate_totals(self):
        total = 0.0
        for item in self.items:
            total += (item.amount or 0.0)
        self.grand_total = round(total, 2)
        # Authoritative 15% VAT for pharmaceuticals in BD standard
        self.vat_amount = round(self.grand_total * 0.15, 2)
        if self.payment_method in ["Credit", "bKash / Nagad"]:
            self.due_amount = self.grand_total
        else:
            self.due_amount = 0.0

    def validate_idempotency(self):
        if self.idempotency_key and self.is_new():
            existing = frappe.db.get_value(
                "Alco Field Order",
                {"idempotency_key": self.idempotency_key},
                "name"
            )
            if existing and existing != self.name:
                frappe.throw(
                    _("Duplicate order detected with idempotency key '{0}'. Existing order: {1}").format(
                        self.idempotency_key, existing
                    ),
                    title=_("Duplicate Order Detected")
                )
