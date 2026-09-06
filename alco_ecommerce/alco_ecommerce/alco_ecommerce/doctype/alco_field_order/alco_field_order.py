import frappe
from frappe.model.document import Document

class AlcoFieldOrder(Document):
    def validate(self):
        """v16 Document validation lifecycle for Alco Field Orders"""
        self.recalculate_totals()

    def recalculate_totals(self):
        total = 0.0
        for item in self.items:
            item.amount = (item.qty or 0) * (item.rate or 0)
            total += item.amount
        self.grand_total = total
