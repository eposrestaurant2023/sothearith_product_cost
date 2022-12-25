# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from py_linq import Enumerable
from frappe.model.document import Document

class Sale(Document):
	def validate(self):
		#validate sale summary
		for d in self.sale_products:
			d.amount = d.quantity * d.price

		total_quantity = Enumerable(self.sale_products).sum(lambda x: x.quantity or 0)
		total_amount = Enumerable(self.sale_products).sum(lambda x: (x.quantity or 0)* (x.price or  0))

		self.total_quantity = total_quantity
		self.total_amount = total_amount
		self.balance = total_amount
		if total_amount == 0:
			frappe.throw("Total amount is 0")
