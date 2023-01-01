# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff,today 

def execute(filters=None):
	if filters.column_group=="Daily":
		n = date_diff(filters.end_date, filters.start_date)
		if n>30:
			frappe.throw("Date range cannot greater than 31 days")

	columns =get_report_columns(filters)
	data = get_report_data(filters)
 
	return columns, data, None, None,None,True

def get_report_columns(filters):
	columns = []
	columns.append({
			"label":"Product",
			"fieldname":"product_name",
			"fieldtype":"Data",	
			"width":350
		})
	dynamic_columns = get_dynamic_report_columns(filters)
	for  d in dynamic_columns:
		 
		columns.append({
			"label":d["label"],
			"fieldname":d["fieldname"],
			"fieldtype":"Currency",	
			"align":"center",
			"width":65
		})
	return columns
 
def get_dynamic_report_columns(filters):
	
	sql = """
				select 
					concat('col_',date_format(date,'%d_%m')) as fieldname, 
					date_format(date,'%d') as label,
					min(date) as date
				from `tabDates` 
				where date between '{}' and '{}'
				group by
					concat('col_',date_format(date,'%d_%m')) , 
					date_format(date,'%d')  	
				order by date
			""".format(filters.start_date, filters.end_date)

	data =  frappe.db.sql(sql, as_dict=1)
	
	return data

def get_report_data(filters):
	dates = get_dynamic_report_columns(filters)
	report_datas = []
	# get district 
	sql = "select distinct district as product_name ,0 as indent, 1 as is_group  from `tabProduct Cost` where {}".format(get_condiction(filters))

	data = frappe.db.sql(sql,filters, as_dict=True)
	
 	# get product
	for d in data:
		report_datas.append(d)
		sql = """
  				select  
      				concat(product_code,'-',product_name) as product_name , 
          			1 as indent  ,
					{0}
             	from `tabProduct Cost` 
              	where 
					district = '{2}' and 
               		{1}"""
		sql = sql.format(get_dynamic_data(dates), get_condiction(filters), d["product_name"])
  
		frappe.msgprint(sql)
		products = frappe.db.sql(sql, filters, as_dict=True)
		for p in products:
			report_datas.append(p)
		# data.append(products)
	 
	
	
	return  report_datas

def get_condiction(filters):
	sql =" posting_date between %(start_date)s and %(end_date)s"
	if filters.district:
		sql = sql + " and district in %(district)s"
	if filters.product_category:
		sql =sql + " and product_category in %(product_category)s" 
	if filters.product:
		sql = sql + " and product_code in %(product)s"
	return sql
	
def get_dynamic_data(dates):
	sqls = []
	for d in dates:
		sqls.append("max(if(posting_date='{}',selling_price,0)) as {}".format(d["date"],d["fieldname"]))
	return ','.join(sqls)
	