import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from frappe.auth import LoginManager
from offline_pos_erpnext.API.v14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
import wrapt


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        # validate_employee(login_manager.user)
        login_manager.post_login()
        if frappe.response["message"] == "Logged In":
            if not frappe.db.exists("Smart Connect User", login_manager.user):
                return gen_response(500, "User has no permission for mobile app, Please Contect Admin")
            
            if frappe.get_value("Smart Connect User", login_manager.user, "enable") == 0:
                return gen_response(500, "User has no permission for mobile app, Please Contect Admin")
            # if frappe.get_doc("Smart Connect User", login_manager.user)
            frappe.response["user"] = login_manager.user
            frappe.response["key_details"] = generate_key(login_manager.user)
            frappe.response["smart_user_details"] = frappe.get_doc('Smart Connect User', login_manager.user)
            frappe.response["user_details"] = frappe.get_doc('User', login_manager.user)
        gen_response(200, frappe.response["message"])
    except frappe.AuthenticationError:
        gen_response(500, frappe.response["message"])
    except Exception as e:
        return exception_handler(e)