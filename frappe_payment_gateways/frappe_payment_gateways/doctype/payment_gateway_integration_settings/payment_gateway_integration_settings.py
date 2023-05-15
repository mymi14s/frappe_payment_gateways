# Copyright (c) 2023, Anthony C. Emmanuel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PaymentGatewayIntegrationSettings(Document):
	
	def validate(self):
		self.check_enabled()

	def get_secret_key(self):
		return self.get_password('secret_key')

	def check_enabled(self):
		"""
			Ensure only one gateway is enabled for each gate type.
		"""
		if self.enabled:
			enabled_gateway = frappe.db.get_list(self.doctype, filters={
				"enabled":1,
				"gateway":self.gateway,
				"name":["!=", self.name]
			},
			fields=["name"])
			if enabled_gateway:
				frappe.throw(f"""
					Another {self.gateway} gateway is enabled, disable it before enabling this one.<br>
					<a class="text-danger" href="/app/{self.doctype.lower().replace(' ', '-')}/{enabled_gateway[0].name}">{enabled_gateway[0].name}</a>
				""")
		
	def get_supported_currency(self):
		return supported_currency.get(self.gateway)


supported_currency = {
	'Paystack': ['NGN', 'GHS', 'ZAR', 'USD']
}