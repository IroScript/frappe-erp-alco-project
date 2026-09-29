import frappe
from alco_ecommerce.api import get_pharma_products, get_orders_list, get_dashboard_summary

def get_context(context):
    context.title = "Alco Pharma Ltd - Admin Operations Portal"
    context.products = get_pharma_products()
    context.orders = get_orders_list()
    context.summary = get_dashboard_summary()
    return context
