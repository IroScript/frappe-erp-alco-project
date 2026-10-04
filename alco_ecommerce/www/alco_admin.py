import frappe
from alco_ecommerce.api import ADMIN_ROLES, get_pharma_products, get_orders_list, get_dashboard_summary

no_cache = 1


def get_context(context):
    # Back-office page: guests go to the standard Frappe login, then come back here.
    # (same redirect pattern core uses in frappe/www/login.py and frappe/www/about.py)
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/alco-admin"
        raise frappe.Redirect
    if not set(ADMIN_ROLES) & set(frappe.get_roles()):
        frappe.throw(frappe._("Not permitted"), frappe.PermissionError)

    # Core only enforces CSRF once the session holds a token (frappe/auth.py validate_csrf_token),
    # so generate it here exactly like frappe/www/desk.py does; the template sends it back as X-Frappe-CSRF-Token.
    context.csrf_token = frappe.sessions.get_csrf_token()

    context.title = "Alco Pharma Ltd - Admin Operations Portal"
    context.products = get_pharma_products()
    context.orders = get_orders_list()
    context.summary = get_dashboard_summary()
    return context
