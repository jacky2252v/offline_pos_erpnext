import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from frappe.auth import LoginManager
from offline_pos_erpnext.API.v14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
import wrapt


@frappe.whitelist(allow_guest = True)
@mtpl_validate(methods=["GET"])

def get_all_item_group():
    try:
        item_group = frappe.get_all(
            "Item Group",
            fields=["*"],
        )
        gen_response(200, "item group get successfully", item_group)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted for item group")
    