# Copyright (c) 2024, Aashish Vashisht and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
        {
            'fieldname': 'invoice_number',
            'label': _('Invoice Number'),
            'fieldtype': 'Link',
            'options': "Sales Invoice",
            'width': '200'
        },
        {
            'fieldname': 'adjustment_amt',
            'label': _('Adjustment Amount'),
            'fieldtype': 'Currency',
            'width': '200'
        },
        {
            'fieldname': 'discount_amt',
            'label': _('Discount Amount'),
            'fieldtype': 'Currency',
            'width': '200'
        },
        {
            'fieldname': 'discount_rate',
            'label': _('Discount Rate'),
            'fieldtype': 'Percent',
            'width': '200'
        },
        {
            'fieldname': 'tax_slab_days',
            'label': _('Tax Slab Days'),
            'fieldtype': 'Int',
            'width': '200'
        },
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND pe.posting_date >= '{}'".format(filters.get("from_date"))
    if filters.get("to_date"):
        conditions += " AND pe.posting_date <= '{}'".format(filters.get("to_date"))
    if filters.get("invoice"):
        conditions += " AND si.name = '{}'".format(filters.get("invoice"))
    
    data = frappe.db.sql(f"""
        SELECT 
            si.name AS invoice_number,
            pr.allocated_amount AS adjustment_amt,
            DATEDIFF(pe.posting_date, si.posting_date) AS tax_slab_days,
            jea.debit_in_account_currency AS discount_amt,
            ROUND((jea.debit_in_account_currency / pr.allocated_amount) * 100, 2) AS discount_rate
        FROM `tabPayment Entry Reference` pr  
        INNER JOIN `tabPayment Entry` pe ON pe.name = pr.parent and pe.docstatus = 1 
        INNER JOIN `tabSales Invoice` si ON si.name = pr.reference_name
        INNER JOIN `tabJournal Entry` je ON je.custom_payment_entry = pe.name AND je.docstatus = 1
        INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name
        WHERE pe.name IS NOT NULL {conditions} 
        GROUP BY pe.name
    """, as_dict=True)
    
    return data

