app_name = "alco_ecommerce"
app_title = "Alco Ecommerce"
app_publisher = "Alco Pharma"
app_description = "Pharmaceutical Field Order & Invoice System"
app_icon = "shopping-bag"
app_color = "#059669"
app_email = "admin@alcopharma.com"
app_license = "mit"
app_logo_url = "/assets/alco_ecommerce/images/alco-ecommerce-logo.svg"
app_home = "/desk/alco-ecommerce"

add_to_apps_screen = [
	{
		"name": "alco_ecommerce",
		"logo": "/assets/alco_ecommerce/images/alco-ecommerce-logo.svg",
		"title": "Alco Ecommerce",
		"route": "/desk/alco-ecommerce",
		"sequence_id": 2,
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk browser
# app_include_css = "/assets/alco_ecommerce/css/alco_ecommerce.css"
# app_include_js = "/assets/alco_ecommerce/js/alco_ecommerce.js"

# Home page
# ----------
home_page = "alco-order"

# Website User Home Page
# ----------------------
# role_home_page = {
# 	"Alco Field Agent": "alco-order",
# }

# Fixtures
# --------
# Custom Fields this app adds to core ERPNext DocTypes (Item, Customer).
# Synced automatically on install and on `bench migrate`
# (local docs: frappe-docs-latest/framework/user/en/guides/app-development/how-to-create-custom-fields-during-app-installation.md).
fixtures = [
	{"dt": "Custom Field", "filters": [["module", "=", "Alco Ecommerce"]]},
]

# Installation
# ------------
# (local docs: frappe-docs-latest/framework/user/en/python-api/hooks.md#install-hooks)
after_install = "alco_ecommerce.install.after_install"
