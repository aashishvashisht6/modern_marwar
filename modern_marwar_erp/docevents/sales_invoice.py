import frappe
from frappe.utils import flt

def before_update_after_submit(doc, method=None):
    old_doc = doc.get_doc_before_save()
    
    if doc.irn and flt(doc.grand_total) != flt(old_doc.grand_total) :
        frappe.throw("Not Permitted")