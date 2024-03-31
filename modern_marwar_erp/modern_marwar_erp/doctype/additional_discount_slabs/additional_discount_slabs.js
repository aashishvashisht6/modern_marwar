// Copyright (c) 2024, Aashish Vashisht and contributors
// For license information, please see license.txt

frappe.ui.form.on("Additional Discount Slabs", {
    setup(frm) {
        frm.set_query("discount_account", () => {
            return {
                filters: {
                    is_group: 0,
                    disabled: 0
                }
            }
        })
    },
});
