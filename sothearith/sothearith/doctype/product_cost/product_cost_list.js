frappe.listview_settings['Product Cost'] = {
    hide_name_column: true,
    has_indicator_for_draft: false,
    onload: function (listview) {
        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Bulk Insert/Update"), function () {
            frappe.route_options = {"product_code": "STEEL0000001"}
            let local_docname = frappe.model.make_new_doc_and_get_name('Bulk Update Product Cost')
            frappe.set_route('Form', 'Bulk Update Product Cost', local_docname, { product_code: 'STEEL0000001' })
        })
        

        // The .addClass above is optional.  It just adds styles to the button.
    }
}