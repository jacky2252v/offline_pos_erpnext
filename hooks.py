app_name = "offline_pos_erpnext"
app_title = "pos"
app_publisher = "offline"
app_description = "offline"
app_email = "midocean@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/offline_pos_erpnext/css/offline_pos_erpnext.css"
# app_include_js = "/assets/offline_pos_erpnext/js/offline_pos_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/offline_pos_erpnext/css/offline_pos_erpnext.css"
# web_include_js = "/assets/offline_pos_erpnext/js/offline_pos_erpnext.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "offline_pos_erpnext/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "offline_pos_erpnext.utils.jinja_methods",
# 	"filters": "offline_pos_erpnext.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "offline_pos_erpnext.install.before_install"
# after_install = "offline_pos_erpnext.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "offline_pos_erpnext.uninstall.before_uninstall"
# after_uninstall = "offline_pos_erpnext.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "offline_pos_erpnext.utils.before_app_install"
# after_app_install = "offline_pos_erpnext.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "offline_pos_erpnext.utils.before_app_uninstall"
# after_app_uninstall = "offline_pos_erpnext.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "offline_pos_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"offline_pos_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"offline_pos_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"offline_pos_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"offline_pos_erpnext.tasks.weekly"
# 	],
# 	"monthly": [
# 		"offline_pos_erpnext.tasks.monthly"
# 	],
# }

after_install = "offline_pos_erpnext.install.after_install"
after_migrate = "offline_pos_erpnext.install.after_install"

# Testing
# -------

# before_tests = "offline_pos_erpnext.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "offline_pos_erpnext.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "offline_pos_erpnext.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["offline_pos_erpnext.utils.before_request"]
# after_request = ["offline_pos_erpnext.utils.after_request"]

# Job Events
# ----------
# before_job = ["offline_pos_erpnext.utils.before_job"]
# after_job = ["offline_pos_erpnext.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"offline_pos_erpnext.auth.validate"
# ]



doc_events = {
    "Customer": {
        "validate": "offline_pos_erpnext.api.customer_validate",
    },
    "Sales Invoice": {
        "autoname": "offline_pos_erpnext.api.sales_invoice_autoname",
    },
    "POS Closing Entry": {
        "autoname": "offline_pos_erpnext.api.pos_closing_autoname",
    },
    "POS Opening Entry":{
        "autoname": "offline_pos_erpnext.api.pos_opening_autoname",
    }
}

fixtures = [
        {"dt": "Role", "filters": {"Is Custom": 1}}
]