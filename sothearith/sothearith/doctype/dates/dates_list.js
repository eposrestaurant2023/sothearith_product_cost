frappe.listview_settings['Dates'] = {
    onload: function (listview) {
        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Generate Date"), function () {
            let d = new frappe.ui.Dialog({
                title: 'Generate Date',
                fields: [
                    {
                        label: 'Start Date',
                        fieldname: 'start_date',
                        fieldtype: 'Date'
                    },
                    {
                        label: 'End Date',
                        fieldname: 'end_date',
                        fieldtype: 'Date'
                    }
                ],
                primary_action_label: 'Save',
                    primary_action(values) {
                        frappe.call({
                            method: "sothearith.sothearith.doctype.dates.dates.generate_date",
                            
                            args: {
                                start_date:values.start_date,
                                end_date:values.end_date
                            },
                            callback: function(r){
                                d.hide();
                            },
                            error: function(r) {
                                frappe.throw(_("Load data fail."))
                                
                            },
                        });	
                    
                }
            });
            
            d.show();
        })
        
        // The .addClass above is optional.  It just adds styles to the button.
    }
}