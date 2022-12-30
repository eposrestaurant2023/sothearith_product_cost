# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Finance(Document):
	@frappe.whitelist()
	def get_summary_information(self):
		total_amount = 0
		total_paid = 0
		balance = 0
		data = frappe.db.sql("select sum(total_amount) as total_amount, sum(total_paid) as total_paid, sum(balance) as balance from `tabSale` where customer='{}' and docstatus =1".format(self.name),as_dict=1)
		if data:
			total_amount =data[0]["total_amount"]
			total_paid =data[0]["total_paid"]
			balance=data[0]["balance"]

		return {
			"total_paid":total_paid,
			"total_amount":total_amount,
			"balance":balance
		}
