import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from offline_pos_erpnext.offline_pos_erpnext.API.V14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
import wrapt

def get_all_payment_list():
    try:
        payment_list = frappe.get_all(
            "Payment Order",
            fields=["*"],
        )
        gen_response(200, "payment list get successfully", payment_list)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted for payment order")
    except Exception as e:
        return exception_handler(e)