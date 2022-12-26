# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days
class BulkUpdateProductCost(Document):
	def on_submit(self):
		
		d = self.start_date
	
		cost =float(self.cost)
		markup =float(self.markup)
		while d<=self.end_date:
			for district in self.districts:
       
				additional_cost = get_additional_cost_by_district(district.district,self.product_code,d)
				data = frappe.db.get_list("Product Cost",{"posting_date":d, "district":district.district, "product_code":self.product_code },["name"])
				if not data:
					selling_price = 0
					total_cost = cost + additional_cost
					if self.markup_type =="Percent":
						selling_price = total_cost + (total_cost * (markup/100))
					else:
						selling_price = total_cost +  markup
			
					doc =frappe.get_doc(
						{
							"doctype":"Product Cost",
							"posting_date":d,
							"district":district.district,
							"product_code":self.product_code,
							"additional_cost":additional_cost,
							"cost":self.cost,
							"markup_type":self.markup_type,
							"markup":self.markup,
							"total_cost":total_cost,
							"selling_price":selling_price,
							"is_bulk_update":1
						}
					)
					doc.insert()
				else:
					
					doc = frappe.get_doc("Product Cost", data[0].name)
					doc.cost = self.cost
					doc.additional_cost = additional_cost
					doc.total_cost = doc.cost + doc.additional_cost
					doc.markup_type = self.markup_type
					if self.disable_update_makup_on_existing_cost ==1:
						doc.markup =self.markup

					doc.is_bulk_update = 1
					if self.markup_type =="Percent":
						doc.selling_price = doc.total_cost + (doc.total_cost * (self.markup/100))
					else:
						doc.selling_price = doc.total_cost +  self.markup
			
					
					doc.save()
		
			d = add_days(d,1)



def get_additional_cost_by_district(district,product, date):
	sql = """
 			select 
    			additional_cost 
       		from `tabDistrict Product Cost` a  
         	where 
          		a.product_code ='{}' and 
            	a.district='{}' and  
             	'{}' between a.start_date and a.end_date 
			order by creation  desc 
   		limit 1""".format(product,district,date)
	 
	data = frappe.db.sql(sql)
	
	if data:
		
		return data[0][0]
	else:
		return 0
     
     
