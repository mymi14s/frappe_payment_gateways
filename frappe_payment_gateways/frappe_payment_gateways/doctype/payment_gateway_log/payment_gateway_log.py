# Copyright (c) 2023, Anthony C. Emmanuel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PaymentGatewayLog(Document):
	
	def after_insert(self):
		if self.status in ['success', 'Success', 'successful']:
			if (frappe.db.exists("Payment Gateway Request", {
				"name":self.payment_gateway_request,
				"status": ["!=", "Paid"]
				})):
				payment_request = frappe.get_doc("Payment Gateway Request", self.payment_gateway_request)
				payment_request.status ='Paid'
				payment_request.submit(ignore_permissions=1)

