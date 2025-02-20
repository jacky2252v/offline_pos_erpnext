import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
from frappe.auth import LoginManager
from offline_pos_erpnext.API.v14.api_utils import gen_response, exception_handler, generate_key, mtpl_validate
import wrapt
import json
from erpnext.stock.utils import get_stock_balance
from frappe.utils import get_fullname, flt

@frappe.whitelist(allow_guest = True)
@mtpl_validate(methods=["GET"])

def get_all_item_list():
    try:
        item_list = []
        items = frappe.get_all("Item", fields=["name"])
        
        for item in items:
            item_doc = frappe.get_doc("Item", item.name)
            
            item_price = frappe.db.get_value(
                "Item Price",
                {"item_code": item.name, "selling": 1},
                ["price_list_rate"],
                as_dict=True
            )
            
            valuation_rate = item_price["price_list_rate"] if item_price else 0
            
            default_warehouse = None
            if item_doc.item_defaults:
                default_warehouse = item_doc.item_defaults[0].default_warehouse
            
            available_qty = 0
            if default_warehouse:
                available_qty = get_stock_balance(
                    item_code=item.name,
                    warehouse=default_warehouse
                ) or 0
            
            item_data = item_doc.as_dict()
            
            item_data.update({
                "valuation_rate": valuation_rate,
                "available_qty": available_qty
            })
            
            item_list.append(item_data)
        
        return gen_response(200, "Item list fetched successfully", item_list)
    except frappe.PermissionError:
        return gen_response(500, "Not permitted to fetch item data")
    except Exception as e:
        return exception_handler(e)


@frappe.whitelist(allow_guest=True)
@mtpl_validate(methods=["GET"])
def get_all_item_list_with_pos_profile(pos_profile):
    try:
        if not pos_profile:
            frappe.throw("Please Select POS Profile")
        
        pos_profile_doc = frappe.get_doc("POS Profile", pos_profile)
        if not pos_profile_doc.warehouse:
            frappe.throw("No Warehouse found in the selected POS Profile")
        
        warehouse = pos_profile_doc.warehouse
        item_list = []
        
        items = frappe.get_all("Item", fields=["name"])
        for item in items:
            item_doc = frappe.get_doc("Item", item.name)
            
            default_warehouse = (
                item_doc.item_defaults[0].default_warehouse
                if item_doc.item_defaults else None
            )
            
            item_price = frappe.db.get_value(
                "Item Price",
                {"item_code": item.name, "selling": 1},
                ["price_list_rate"],
                as_dict=True
            )
            valuation_rate = item_price["price_list_rate"] if item_price else 0
            
            available_qty = get_stock_balance(
                item_code=item.name,
                warehouse=warehouse
            ) or 0
            
            item_data = item_doc.as_dict()
            item_data.update({
                "valuation_rate": valuation_rate,
                "available_qty": available_qty
            })
            item_list.append(item_data)
    
        return gen_response(200, "Item list fetched successfully", item_list)
    
    except frappe.PermissionError:
        return gen_response(500, "Not permitted to fetch item data")
    except Exception as e:
        return exception_handler(e)


def create_item_list():
    res = {}        
    try:     
        a = json.loads(frappe.request.data)
        x = frappe.session.user
        doc = frappe.new_doc('item_list')
        doc.item = a['item']
        doc.uom = a['uom']
        doc.qty = a['qty']
        doc.warehouse = a['warehouse']
        doc.user = x
        # doc.stock_reconciliation = a['stock_reconciliation']
        doc.batch = a['batch']
        doc.save()
        # add_item_list_details(a['item'], a['warehouse'], a['stock_reconciliation'], a['batch'])
        # publish_data_real_time(a['item'], a['warehouse'], a['stock_reconciliation'], a['uom'], a['batch'])
        print(a)
        res['apicode'] = 1
        res['data'] = "1"
    except Exception as e:
        raise e
    return res
    
def publish_data_real_time(item, warehouse, stock_reconciliation, uom, batch=None, serial_no=None):
    qty = frappe.db.sql(
        """ select SUM(tsrl.qty) from `item_list` tsrl where tsrl.item = '{0}' and tsrl.warehouse = '{1}' and tsrl.stock_reconciliation = '{2}' """.format(
            item, warehouse, stock_reconciliation))
    data = {'stock_reconciliation': stock_reconciliation, 'item': item, 'warehouse': warehouse,
            'qty': flt(qty[0][0]),
            'uom': uom, 'batch': batch, 'serial_no': serial_no}
    frappe.publish_realtime('item_list', data)