# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from py_linq import Enumerable
class DistrictCost(Document):
	def validate(self):
		self.total_cost =  Enumerable(self.costs).sum(lambda x: x.cost or 0)
		if (self.total_cost or 0) ==0:
			frappe.throw(_("Please enter cost"))
   
   
		for p in self.products:
			p.district = self.district
			p.start_date = self.start_date
			p.end_date= self.end_date
			p.additional_cost= self.total_cost
   
	def on_submit(self):
		
		sql = """
  				update `tabProduct Cost` 
      			set 
         			additional_cost = {0}, 
            		total_cost  = cost + {0} ,
					selling_price = if(markup_type='Percent',(cost+{0})+((cost + {0})* markup/100),(cost+{0} + markup)) 
				where 
    				posting_date between '{1}' and '{2}' and 
					district='{3}' and 
					product_code in (select product_code from `tabDistrict Product Cost` where parent ='{4}')
     		"""
		sql=sql.format(self.total_cost,self.start_date, self.end_date, self.district,self.name)
		#frappe.throw(sql)
		frappe.db.sql(sql)
		frappe.db.commit()
 