import frappe
import datetime
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from frappe.auth import LoginManager
from offline_pos_erpnext.API.v14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
from frappe.utils.password import check_password
from erpnext.stock.utils import get_stock_balance

@frappe.whitelist()
def sales_invoice_autoname(doc,method):
    if doc.is_pos:
        if doc.pos_invoice_name:
            doc.name = doc.pos_invoice_name

@frappe.whitelist()
def pos_closing_autoname(doc,method):
    if doc.naming_series:
        doc.name = doc.naming_series

@frappe.whitelist()
def pos_opening_autoname(doc,method):
    if doc.naming_series:
        doc.name = doc.naming_series

@frappe.whitelist(allow_guest = True)
def check_user_password(user, pwd):
    """Check if the provided password is correct for the user"""
    try:
        # Use check_password to verify the user's password
        return check_password(user, pwd)
    except frappe.AuthenticationError:
        frappe.throw("Incorrect password for user: {0}".format(user))

@frappe.whitelist(allow_guest = True)
def get_setting():
    try:
        default_company = frappe.db.get_single_value("Global Defaults", "default_company")
        
        if not default_company:
            return gen_response(404, "Default company not found", None)

        company_address_name = frappe.get_value("Dynamic Link", {"link_doctype": "Company", "link_name": default_company}, "parent")
        company_address = frappe.get_value("Address", company_address_name, ["address_line1", "address_line2", "city", "state", "country", "pincode", "email_id", "phone"], as_dict=True)

        if not company_address:
            return gen_response(404, "Company address not found", None)

        pos_profiles = frappe.get_all("POS Profile", fields=["name"])

        if not pos_profiles:
            return gen_response(404, "No POS Profile documents found", None)

        res = {
            "default_company": default_company,
            "company_address": company_address,
            "pos_profiles": [profile.name for profile in pos_profiles]
        }

        return gen_response(200, "Data retrieved successfully", res)

    except frappe.DoesNotExistError:
        return gen_response(404, "Data not found", None)

    except Exception as e:
        return exception_handler(e)


def gen_response(status, message, data=None):
    response = {
        'status': status,
        'message': message,
        'data': data
    }
    return response

def exception_handler(e):
    return gen_response(500, str(e))

@frappe.whitelist(allow_guest = True)
def get_customer_list():
    try:
        customers = []
        cus_list = frappe.get_all("Customer")
        
        for x in cus_list:
            cus_doc = frappe.get_doc("Customer", x.name)
            
            link_docs = frappe.get_all("Dynamic Link", 
                                       filters={'link_doctype': 'Customer', 'link_name': cus_doc.name, 'parenttype': 'Address'},
                                       fields=['parent'])
            
            address_details = {
                'address_line1': None,
                'address_line2': None,
                'city': None,
                'state': None,
                'zip_code': None,
                'country': None
            }
            
            if link_docs:
                address_name = link_docs[0].parent
                if frappe.db.exists("Address", address_name):
                    address_doc = frappe.get_doc("Address", address_name)
                    address_details = {
                        'address_line1': address_doc.address_line1,
                        'address_line2': address_doc.address_line2,
                        'city': address_doc.city,
                        'state': address_doc.state,
                        'zip_code': address_doc.pincode,
                        'country': address_doc.country
                    }
            
            customers.append({
                'name': cus_doc.name,
                'territory': cus_doc.territory,
                'customer_group': cus_doc.customer_group,
                'customer_type': cus_doc.customer_type,
                'email_id': cus_doc.email_id,
                'mobile_no': cus_doc.mobile_no,
                'customer_name': cus_doc.customer_name,
                **address_details
            })
        
        return gen_response(200, "Customer list fetched successfully", customers)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted to access Customer data")
    except Exception as e:
        return exception_handler(e)


@frappe.whitelist(allow_guest = True)
def get_fifo_serial_no(item_code):
    try:
        serial_no = frappe.get_all(
            "Serial No",
            filters={'item_code': item_code},
            fields=['name'],
            order_by='creation asc',
            limit=1
        )
        
        if not serial_no:
            return gen_response(404, "No serial number found for the given item code")
        
        return gen_response(200, "Serial number fetched successfully", serial_no[0].name)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted to access Serial No data")
    except Exception as e:
        return exception_handler(e)
    

@frappe.whitelist(allow_guest = True)
def check_opening_entry(user):
    try:
        today = datetime.date.today()
        
        open_entries = frappe.get_all(
            "POS Opening Entry",
            filters={
                "user": user,
                "status": "Open",
                "posting_date": today,
                "pos_closing_entry": ["in", ["", None]],
                "docstatus": 1
            },
            fields=["name"]
        )
        
        if open_entries:
            return True
        else:
            return False
        
    except Exception as e:
        return exception_handler_new(e)

def exception_handler_new(e):
    return False  

    
@frappe.whitelist(allow_guest=True)
def custom_login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()

        if frappe.response.get("message") != "Logged In":
            return gen_response(401, _("Login failed"))

        company = frappe.defaults.get_user_default("company")
        desktop_pos_setting = frappe.get_single("Desktop POS Setting")
        
        walk_in_customer = None
        default_company = None
        taxes_and_charges = None
        pos_profile_warehouse = None

        if desktop_pos_setting:
            walk_in_customer = desktop_pos_setting.walk_in_customer
            default_company = desktop_pos_setting.default_pos_profile

            if default_company:
                pos_profile_doc = frappe.get_doc("POS Profile", default_company)
                taxes_and_charges = pos_profile_doc.sales_taxes_and_charges_template
                pos_profile_warehouse = pos_profile_doc.warehouse

        if walk_in_customer and default_company:
            return gen_response(200, _("Login successful"), {
                "default_company": default_company,
                "Walk In Customer": walk_in_customer,
                "company": company,
                "pos_profile_taxes_and_charges":taxes_and_charges,
                "pos_profile_warehouse":pos_profile_warehouse
            })

        return gen_response(200, _("Login successful"), {
            "default_company": default_company,
            "Walk In Customer": _("Please select Walk-In Customer and POS Profile in Desktop POS Setting")
        })

    except frappe.AuthenticationError:
        return gen_response(401, _("Invalid username or password"))
    except Exception as e:
        return exception_handler(e)

    
@frappe.whitelist(allow_guest = True)
def validate_password(password):
    try:
        current_user = frappe.session.user

        frappe.local.login_manager.authenticate(current_user, password)

        return gen_response(200, "Password validated successfully", True)

    except frappe.AuthenticationError:
        return gen_response(200, "Password does not match", False)

    except frappe.DoesNotExistError:
        return gen_response(404, "Current user not found", None)

    except Exception as e:
        return exception_handler(e)
    
@frappe.whitelist(allow_guest = True)
def get_pos_profile_password():
    try:
        default_pos_profile = frappe.defaults.get_user_default("POS Profile")
        
        if not default_pos_profile:
            return gen_response(404, "POS Profile not found for current user", None)

        pos_profile = frappe.get_doc("POS Profile", default_pos_profile)

        str_password = pos_profile.get_password('master_password', raise_exception=False)

        if not str_password:
            return gen_response(404, "Master password not set or found", None)

        return gen_response(200, "Master password retrieved successfully", str_password)

    except frappe.DoesNotExistError:
        return gen_response(404, "POS Profile or master password not found", None)

    except Exception as e:
        return exception_handler(e)


@frappe.whitelist(allow_guest = True)
def customer_validate(self, method):
    if self.is_new():
        if self.address_line_1 and self.city: 
    
            Customer_add = frappe.new_doc('Address')

            Customer_add.address_title  = self.customer_name

            Customer_add.address_line1  = self.address_line_1
            Customer_add.address_line2  = self.address_line_2
            Customer_add.phone  = self.contact_number
            Customer_add.email_id = self.email_id1
            Customer_add.city  = self.city
            Customer_add.state  = self.state
            Customer_add.zip_code  = self.zip_code
            Customer_add.country  = self.country
            Customer_add.save()


# @frappe.whitelist()
# def get_offline_pos_users_with_tokens():
#     try:
#         users = frappe.db.sql("""
#             SELECT DISTINCT user.full_name, user.email, user.username, user.offline_pos_password
#             FROM `tabUser` AS user
#             JOIN `tabHas Role` AS role ON user.name = role.parent
#             WHERE role.role = 'Offline POS User' AND user.enabled = 1
#         """, as_dict=True)

#         if not users:
#             return gen_response(404, "No users found with the role 'Offline POS User'", None)

#         for user in users:
#             user_token = frappe.generate_hash(user.name) 

#             user.update({
#                 "token": user_token,
#             })

#         return gen_response(200, "Users fetched successfully", users)

#     except Exception as e:
#         return exception_handler(e)

@frappe.whitelist()
def get_offline_pos_users_with_tokens():
    try:
        users = frappe.db.sql("""
            SELECT DISTINCT 
                user.full_name, 
                user.email, 
                user.username, 
                user.offline_pos_password, 
                auth.password AS token
            FROM `tabUser` AS user
            JOIN `tabHas Role` AS role ON user.name = role.parent
            LEFT JOIN `__Auth` AS auth ON user.name = auth.name 
                AND auth.doctype = 'User' 
                AND auth.fieldname = 'password'
            WHERE role.role = 'Offline POS User' 
            AND user.enabled = 1
        """, as_dict=True)

        if not users:
            return gen_response(404, "No users found with the role 'Offline POS User'", None)

        return gen_response(200, "Users fetched successfully", users)

    except Exception as e:
        return exception_handler(e)

@frappe.whitelist()
def get_available_stock(item_code, pos_profile, warehouse=None):
    try:
        pos_profile_doc = frappe.get_doc("POS Profile", pos_profile)
        available_qty = get_stock_balance(item_code, pos_profile_doc.warehouse)

        if not available_qty:
            return gen_response(404, "No available stock found for the item", None)

        return gen_response(200, "Stock fetched successfully", available_qty)

    except Exception as e:
        return exception_handler(e)

@frappe.whitelist()
def get_available_stock_for_all_items(pos_profile):
    try:
        pos_profile_doc = frappe.get_doc("POS Profile", pos_profile)

        target_warehouse = pos_profile_doc.warehouse

        items = frappe.get_all("Item", fields=["item_code", "item_name"])

        available_stock_list = []

        for item in items:
            available_qty = get_stock_balance(item["item_code"], target_warehouse)

            available_stock_list.append({
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "available_qty": available_qty
            })

        if not available_stock_list:
            return gen_response(404, "No available stock found for any items", None)

        return gen_response(200, "Stock fetched successfully", available_stock_list)

    except Exception as e:
        return exception_handler(e)

