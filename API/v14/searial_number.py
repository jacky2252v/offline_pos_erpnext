import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from offline_pos_erpnext.offline_pos_erpnext.API.V14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
import wrapt

def get_all_searial_number_list():
    try:
        searial_number_list = frappe.get_all(
            "Searial Number Order",
            fields=["*"],
        )
        gen_response(200, "searial number list get successfully", searial_number_list)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted for searial number order")
    except Exception as e:
        return exception_handler(e)