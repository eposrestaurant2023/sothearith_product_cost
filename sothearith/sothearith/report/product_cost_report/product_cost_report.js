
frappe.query_reports["Product Cost Report"] = {
	
	"filters": [
		
		
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			 
		
		},
	 
		{
			"fieldname": "district",
			"label": __("District"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('District', txt);
			}
		} ,
		{
			fieldname: "product_category",
			label: __("Category"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Product Category', txt);
			}
			 
		},
		 
		{
			fieldname: "product",
			label: __("Product"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Product', txt);
			}
			 
		},
		 

	],
	"formatter": function(value, row, column, data, default_formatter) {
	
		value = default_formatter(value, row, column, data);
		 
		if(data[column["fieldname"]]== 0 || data[column["fieldname"]] == undefined ){
			value = $(`<span></span>`);

		var $value = $(value).css("font-weight", "normal");
		

		value = $value.wrap("<p></p>").parent().html();
		}
		if (data && data.is_group==1 ) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			

			value = $value.wrap("<p></p>").parent().html();
		}
			
		

	
		
		return value;
	},
	
};

 