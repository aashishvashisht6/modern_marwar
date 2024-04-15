import frappe
from frappe.utils import date_diff, flt 
from frappe import _

def on_submit(doc, event=None):
    if doc.get('references') and doc.get("party_type") == "Customer" and doc.get("payment_type") == "Receive": 
            
        for document in doc.get("references"): 
            if document.get("reference_doctype") == "Sales Invoice":
                si_doc = frappe.db.get_value("Sales Invoice", document.get('reference_name'), 
                                             ["custom_discount_applicable","custom_additional_discount_slab",
                                              "posting_date"], as_dict=1)
                
                if si_doc.custom_discount_applicable:
                    reference_name = document.get("reference_name")
                    dateDiff = date_diff(doc.posting_date, si_doc.posting_date)
                    discount_per = frappe.db.get_value("Discount Slab Days",filters={"parent": si_doc.custom_additional_discount_slab,
                                                                      "days": dateDiff},fieldname="discount")
                    discount_amount = (flt(document.get('allocated_amount')) * flt(discount_per)) /100
                    
                    outstanding_amt = flt(document.get('outstanding_amount'))
                    
                    if discount_amount > 0:
                        accounts = [
                                    {
                                    "account": frappe.db.get_value("Additional Discount Slabs", filters={"name":si_doc.custom_additional_discount_slab}, fieldname="discount_account"),
                                    "debit_in_account_currency": discount_amount
                                    }
                                    ]
                        
                        if outstanding_amt >= discount_amount:
                            reference_name = document.get("reference_name")
                            accounts.append({
                                "account": frappe.db.get_value("Account", filters={"account_name":"Debtors", "company":doc.company}, fieldname="name"),
                                "party_type": "Customer",
                                "party": doc.party,
                                "reference_type": "Sales Invoice",
                                "reference_name": reference_name,
                                "credit_in_account_currency": discount_amount,
                            })
                        elif outstanding_amt < 1:
                            accounts.append({
                                "account": frappe.db.get_value("Account", filters={"account_name":"Debtors", "company":doc.company}, fieldname="name"),
                                "party_type": "Customer",
                                "party": doc.party,
                                "credit_in_account_currency": discount_amount,
                            })
                        elif outstanding_amt != 0 and outstanding_amt > 0:
                            reference_name = document.get("reference_name")
                            accounts.append({
                                "account": frappe.db.get_value("Account", filters={"account_name":"Debtors", "company":doc.company}, fieldname="name"),
                                "party_type": "Customer",
                                "party": doc.party,
                                "reference_type": "Sales Invoice",
                                "reference_name": document.get('reference_name'),
                                "credit_in_account_currency": outstanding_amt,
                            })
                            accounts.append({
                                "account": frappe.db.get_value("Account", filters={"account_name":"Debtors", "company":doc.company}, fieldname="name"),
                                "party_type": "Customer",
                                "party": doc.party,
                                "credit_in_account_currency": discount_amount - outstanding_amt,
                            })
                            
                        
                        je_doc = frappe.get_doc({
                                        "doctype":"Journal Entry",
                                        "voucher_type": "Journal Entry",
                                        "posting_date": doc.posting_date,
                                        "company": doc.company,
                                        "accounts": accounts
                                    })
                        je_doc.custom_payment_entry = doc.name
                        je_doc.save(ignore_permissions=True)
                        je_doc.submit()  
                        frappe.msgprint(
                        _("Additional Discount {0} adjusted against {1}").format(discount_amount,reference_name),
                        indicator="green",
                        alert=True,
                    )
                        
                        
def validate(doc, event=None):
    if doc.get('references') and doc.get("party_type") == "Customer" and doc.get("payment_type") == "Receive": 
        doc_references = doc.get("references")
        doc.references = []
        for document in doc_references: 
            if document.get("reference_doctype") == "Sales Invoice":
                si_doc = frappe.db.get_value("Sales Invoice", document.get('reference_name'), 
                                             ["custom_discount_applicable","custom_additional_discount_slab",
                                              "posting_date"], as_dict=1)
                
                if si_doc.custom_discount_applicable:
                    reference_name = document.get("reference_name")
                    
                    dateDiff = date_diff(doc.posting_date, si_doc.posting_date)

                    
                    discount_per = frappe.db.get_value("Discount Slab Days",filters={"parent": si_doc.custom_additional_discount_slab,
                                                                      "days": dateDiff},fieldname="discount")
                    
                    discount_amount = (flt(document.get('allocated_amount')) * flt(discount_per)) /100
                    
                    document.update({"custom_discount_amount": discount_amount})
                    
                    if discount_amount > 0:
                        frappe.msgprint(
                        _("Additional Discount {0} is applicable on {1}").format(discount_amount,reference_name),
                        indicator="green",
                        alert=True,
                    )
            doc.append("references", document)