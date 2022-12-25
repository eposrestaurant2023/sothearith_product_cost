// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale Payment", {
    setup(frm) {
        frm.set_query("sale", function() {
            return {
                filters: [
                    ["Sale","docstatus", "=", 1]
                ]
            }
        });
    }
});
