// Copyright (c) 2024, Aashish Vashisht and contributors
// For license information, please see license.txt

frappe.query_reports["Invoice Additional Discounts"] = {
    "filters": [
        {
            "fieldname": "invoice",
            "label": __("Invoice Number"),
            "fieldtype": "Link",
            "options": "Sales Invoice"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.now_date(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date(),
            "reqd": 1
        }
    ]
};
