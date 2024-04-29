// Copyright (c) 2024, Aashish Vashisht and contributors
// For license information, please see license.txt

frappe.ui.form.on("Barcode Print", {
    item_code(frm) {
        if (frm.doc.item_code) {
            frappe.db.get_doc("Item", frm.doc.item_code).then(resp => {
                const color_row = resp?.attributes?.filter(row => row.attribute === "Colour" || row.attribute === "Color")
                if (color_row.length > 0) {
                    frm.set_value("colour", color_row[0].attribute_value)
                }
            })

        }
    },
    size: frm => {
        if (frm.doc.size) {
            frm.set_df_property("meter", "hidden", 1)
        }
        else {
            frm.set_df_property("meter", "hidden", 0)
        }
    },
    meter: frm => {
        if (frm.doc.meter) {
            frm.set_df_property("size", "hidden", 1)
        }
        else {
            frm.set_df_property("size", "hidden", 0)
        }
    }
});
