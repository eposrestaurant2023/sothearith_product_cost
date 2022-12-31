// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale", {
	refresh(frm) {
        if(frappe.user.has_role("Sothearith HR")){ 
			frm.set_query("customer_type", function() {
				return {
					filters: [["DocType","name","in",["Executive","Chairman","Cost Controller","Labor","","Driver","Production","Front Office","Purchasing","Human Resource","Sale and Marketing","Accounting","Finance","Law","Stock Control","IT and Maintenance"]]]
				}
			});
		}else{
			return {
				filters: [["DocType","name","in",["Customer","Customer Contractor","Customer Depot","Customer Project"]]]
			}
		}
	},
});

frappe.ui.form.on('Sale Products', {
	product_code(frm,cdt, cdn) {
		update_products_amount(frm,cdt,cdn);
	},
    quantity(frm,cdt, cdn) {
		update_products_amount(frm,cdt,cdn);
	},
    price(frm,cdt, cdn) {
		update_products_amount(frm,cdt,cdn);
	},
})

function update_products_amount(frm,cdt, cdn)  {
    let doc = locals[cdt][cdn];
		if(doc.quantity < 1) doc.quantity = 1;
		doc.amount=doc.quantity * doc.price;
	    frm.refresh_field('sale_products');
		updateSumTotal(frm);
}

function updateSumTotal(frm) {
    
    let sum_total = 0;
	let total_qty = 0;
  
    $.each(frm.doc.sale_products, function(i, d) {
        sum_total += flt(d.amount);
		total_qty +=flt(d.quantity);
		 
    });
	
    
    frm.set_value('total_amount', sum_total);
    frm.set_value('total_quantity', total_qty);
   
	frm.refresh_field("total_amount");
	frm.refresh_field("total_quantity");
}