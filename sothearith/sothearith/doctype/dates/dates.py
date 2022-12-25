# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import add_days
from dateutil import parser
class Dates(Document):
	pass

@frappe.whitelist()
def generate_date(start_date, end_date):
	start_date = parser.parse(start_date)
	end_date = parser.parse(end_date)
	d = start_date
 
	while d<=end_date:
		data = frappe.db.get_list("Dates",{"date":d},["date"])
		if not data:
			doc =frappe.get_doc(
				{
					"doctype":"Dates",
					"date":d
				}
			)
			doc.insert()
		d = add_days(d,1)

	# frappe.db.commit()	