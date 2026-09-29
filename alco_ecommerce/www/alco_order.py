import frappe
from alco_ecommerce.api import get_pharma_products

no_cache = 1

def get_context(context):
    context["title"] = "Alco Pharma - Field Staff Ordering Portal"
    context["products"] = get_pharma_products()
    return context
