// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer Project", {
    refresh(frm) {
        set_indicator(frm);
            },
        });
        
        function set_indicator(frm){
            if(frm.doc.__islocal)
                    return;
            
            frm.call({
                method: 'get_summary_information',
                doc:frm.doc,
                callback:function(r){
                    
                    if(r.message){
                        
                            frm.dashboard.add_indicator(__("Total Sale: {0}",[format_currency(r.message.total_amount)]) ,"green");
                            frm.dashboard.add_indicator(__("Total Paid: {0}",[format_currency(r.message.total_paid)]) ,"green");
                            frm.dashboard.add_indicator(__("Balance: {0}",[format_currency(r.message.balance)]) ,"green");
                         
        
                    }
                    
                },
                async: true,
            });
        }
        