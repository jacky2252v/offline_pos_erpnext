import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

@frappe.whitelist(allow_guest = True)
def after_install():
    custom_field_pos_profile()
    custom_field_customer()
    custom_field_pos_invoice()

def custom_field_pos_profile():
    create_custom_field(
        "POS Profile",
        {
            "label": _("Master Password"),
            "fieldname": "master_password",
            "fieldtype": "Password",
            "insert_after": "warehouse",
        },
    )
    create_custom_field(
        "POS Profile",
        {
            "label": _("Sales Taxes and Charges Template"),
            "fieldname": "sales_taxes_and_charges_template",
            "fieldtype": "Link",
            "options":"Sales Taxes and Charges Template",
            "insert_after": "master_password",
        },
    )
    create_custom_field(
        "POS Opening Entry",
        {
            "label": _("Naming Series"),
            "fieldname": "naming_series",
            "fieldtype": "Data",
            "insert_after": "column_break_3",
        },
    )

    create_custom_field(
            "POS Closing Entry",
            {
                "label": _("Naming Series"),
                "fieldname": "naming_series",
                "fieldtype": "Data",
                "insert_after": "column_break_3",
            },
        )

def custom_field_customer():
    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Offline POS"),
    #          "fieldname": "offline_pos",
    #          "fieldtype": "Section Break",
    #          "insert_after": "account_manager",
    
    #     },
    # )

    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Contact Number"),
    #          "fieldname": "contact_number",
    #          "fieldtype": "Data",
    #          "insert_after": "offline_pos",
    #          "options": "Phone",
    
    #     },
    # )

    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Email ID"),
    #          "fieldname": "email_id1",
    #          "fieldtype": "Data",
    #          "insert_after": "contact_number",
    #          "options": "Email",
    
    #     },
    # )
    create_custom_field(
         "User",
         {
             "label": _("Offline POS Password"),
             "fieldname": "offline_pos_password",
             "fieldtype": "Data",
             "insert_after": "api_key",
    
        },
    )

    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Address Line 1"),
    #          "fieldname": "address_line_1",
    #          "fieldtype": "Data",
    #          "insert_after": "contact_number",
    
    #     },
    # )
    
    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Address Line 2"),
    #          "fieldname": "address_line_2",
    #          "fieldtype": "Data",
    #          "insert_after": "address_line_1",
    
    #     },
    # )
    
    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("City"),
    #          "fieldname": "city",
    #          "fieldtype": "Data",
    #          "insert_after": "address_line_2",
    
    #     },
    # )

    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("State"),
    #          "fieldname": "state",
    #          "fieldtype": "Data",
    #          "insert_after": "city",
    
    #     },
    # )

    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Zip Code"),
    #          "fieldname": "zip_code",
    #          "fieldtype": "Data",
    #          "insert_after": "state",
    
    #     },
    # )

    # create_custom_field(
    #      "Customer",
    #      {
    #          "label": _("Contry"),
    #          "fieldname": "country",
    #          "fieldtype": "Data",
    #          "insert_after": "zip_code",
    
    #     },
    # )


def custom_field_pos_invoice():
    create_custom_field(
         "POS Invoice",
         {
             "label": _("Offline POS"),
             "fieldname": "offline_pos",
             "fieldtype": "Section Break",
             "insert_after": "due_date",
    
        },
    )

    create_custom_field(
         "POS Invoice",
         {
             "label": _("POS Invoice Name"),
             "fieldname": "pos_invoice_name",
             "fieldtype": "Data",
             "insert_after": "offline_pos",
    
        },
    )

    create_custom_field(
         "POS Invoice",
         {
             "label": _("POS Invoice ID"),
             "fieldname": "pos_invoice_id",
             "fieldtype": "Data",
             "insert_after": "pos_invoice_name",
    
        },
    )
    create_custom_field(
         "Sales Invoice",
         {
             "label": _("POS Invoice Name"),
             "fieldname": "pos_invoice_name",
             "fieldtype": "Data",
             "insert_after": "is_pos",
             "depends_on":"eval:doc.is_pos == 1;"
    
        },
    )

    create_custom_field(
         "Sales Invoice",
         {
             "label": _("POS Invoice ID"),
             "fieldname": "pos_invoice_id",
             "fieldtype": "Data",
             "insert_after": "pos_invoice_name",
             "depends_on":"eval:doc.is_pos == 1;"
    
        },
    )