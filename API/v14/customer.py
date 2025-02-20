import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from frappe.auth import LoginManager
from offline_pos_erpnext.API.v14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
import wrapt


@frappe.whitelist(allow_guest = True)
def get_all_customer_list():
    try:
        customer_list = frappe.get_all(
            "Customer",
            fields=["*"],
        )
        gen_response(200, "customer list get successfully", customer_list)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted for customer order")
    except Exception as e:
        return exception_handler(e)