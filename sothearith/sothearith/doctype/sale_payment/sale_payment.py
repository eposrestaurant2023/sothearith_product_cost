# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalePayment(Document):
	def validate(self):
		#validate expense if is a submitted expense
		sale_status = frappe.db.get_value("Sale",self.sale,"docstatus")
		
		if not sale_status==1:
			frappe.throw("This sale is not submitted yet")

		#check paid amount cannot over balance
		if self.payment_amount > self.balance:
			frappe.throw("Payment amount cannot greater than purchase balance")

	def on_submit(self):
		update_sale(self)

	
	def on_cancel(self):
		update_sale(self)


def update_sale(self):
	data = frappe.db.sql("select  ifnull(sum(payment_amount),0)  as total_paid from `tabSale Payment` where docstatus=1 and sale='{}'".format(self.sale))
	sale_amount = frappe.db.get_value('Sale', self.sale, 'total_amount')
	
	if data and sale_amount:
		frappe.db.set_value('Sale', self.sale,  {
			'total_paid': data[0][0] ,
			'balance': sale_amount - data[0][0]  
		})
