# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import add_days
 
from dateutil import parser
from frappe.model.document import Document

class ProductCost(Document):
	def validate(self):
		 
		if self.is_bulk_update==0:
			if self.is_new():
				if frappe.db.exists("Product Cost", {"posting_date":self.posting_date, "district":self.district,"product_code":self.product_code}):
					frappe.throw("Product cost on {} already exist".format(self.posting_date))
			
			self.additional_cost  = get_additional_cost_by_district ( self.district,self.posting_date)
 
			self.total_cost = self.cost + self.additional_cost
			if self.markup_type =="Percent":
				self.selling_price =self.total_cost + (self.total_cost * (self.markup/100))
			else:
				self.selling_price = self.total_cost +  self.markup
    


@frappe.whitelist()
def bulk_update(start_date, end_date, district, product_code, cost,markup_type="Percent", markup=None):
	if not start_date:
		frappe.throw("Please enter start date")
  
	if not end_date:
		frappe.throw("Please enter end date")
  
	if not district:
		frappe.throw("Please enter district")
  
	if not product_code:
		frappe.throw("Please enter product_code")
   
  
	if not (markup or 0):
		frappe.throw("Please enter markup")
  
	start_date = parser.parse(start_date)
	end_date = parser.parse(end_date)
	d = start_date

	additional_cost = 100
 
	cost =float(cost)
	markup =float(markup)
	while d<=end_date:
		additional_cost = get_additional_cost_by_district(district,d)
		
		data = frappe.db.get_list("Product Cost",{"posting_date":d, "district":district, "product_code":product_code },["name"])
		if not data:
			selling_price = 0
			total_cost = cost + additional_cost
			if markup_type =="Percent":
				selling_price = total_cost + (total_cost * (markup/100))
			else:
				selling_price = total_cost +  markup
    
			doc =frappe.get_doc(
				{
					"doctype":"Product Cost",
					"posting_date":d,
					"district":district,
					"product_code":product_code,
					"additional_cost":additional_cost,
					"cost":cost,
					"markup_type":markup_type,
					"markup":markup,
					"total_cost":total_cost,
					"selling_price":selling_price
				}
			)
			doc.insert()
		else:
			doc = frappe.get_doc("Product Cost", data[0].name)
			doc.cost = cost
			doc.additional_cost = additional_cost
			doc.total_cost = doc.cost + doc.additional_cost
			doc.markup_type = markup_type
			doc.markup = markup
			if markup_type =="Percent":
				doc.selling_price = doc.total_cost + (doc.total_cost * (markup/100))
			else:
				doc.selling_price = doc.total_cost +  markup
    
			doc.save()
   
		d = add_days(d,1)

def get_additional_cost_by_district(district, date):
	sql = "select total_cost from `tabDistrict Cost` a  where a.district='{}' and  '{}' between a.start_date and a.end_date order by a.end_date desc limit 1".format(district,date)
	 
	data = frappe.db.sql(sql)
	if data:
		return data[0][0]
	else:
		return 0