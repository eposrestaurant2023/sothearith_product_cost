// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("District Cost", {
	refresh(frm) {
        if (frm.is_new()){
           
            if(!frm.doc.costs){ 
            frappe.db.get_list('Cost Code', {
                fields: ['cost_code'],
               
            }).then(rows => {
                $.each(rows,function(i, d)  {
                    let doc = frm.add_child("costs");
                    doc.cost = 0;
                    doc.cost_code = d.cost_code;
                   
                } );
                frm.refresh_field('costs'); 
            })
        }
            
          
        }
	},
});

frappe.ui.form.on('District Additional Cost', {
    cost(frm,cdt, cdn) {
        const row = locals[cdt][cdn];
        let cost_code_list = frm.doc.costs;
        frm.set_value('total_cost', cost_code_list.reduce((n, d) => n + d.cost,0));

    }
});
