# Copyright (c) 2023, Anthony C. Emmanuel and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe_payment_gateways.frappe_payment_gateways.doctype.payment_gateway_integration_settings.payment_gateway_integration_settings import supported_currency

class PaymentGatewayRequest(Document):
	def after_insert(self):
		self.send_payment_request()
	
	def validate(self):
		self.validate_currency()
		if not self.payment_url:
			self.payment_url = f"""{frappe.utils.get_url()}/payment/pay?id={self.name}"""

	def before_submit(self):
		if self.status!="Paid":
			frappe.throw("Unpaid request cannot be submitted.")

	def validate_currency(self):
		# check for supported currency
		currencies = supported_currency.get(self.gateway)
		if not currencies:
			frappe.throw("No supported currency found for the selected gateway.")
		if not self.currency in currencies:
			frappe.throw(f"""
				{self.gateway} gateway only support currencies {currencies}
			""")

	def send_payment_request(self):
		subject = self.subject.format(doc=self)
		message = self.message.format(doc=self)
		frappe.sendmail(
			recipients=[self.email],
			subject=self.subject,
			message=message,
		)

	@frappe.whitelist()
	def get_amount(self, doc):
		doc = frappe._dict(doc)
		try:
			amount = frappe.db.get_value(doc.reference_doctype, doc.reference_name, 'grand_total')
			if amount:return amount
			amount = frappe.db.get_value(doc.reference_doctype, doc.reference_name, 'total')
			if amount:return amount
		except:
			amount = 0
		return amount
	
@frappe.whitelist()
def make_payment_gateway_request(source_name, target_doc = None):
	args = frappe._dict(json.loads(frappe.form_dict.args))

	def set_missing_values(source, target):
		target.reference_doctype = source.doctype
		target.reference_name = source.name
		target.amount = source.grand_total
		target.cost_center = source.cost_center
		target.currency = source.currency
	
	doc = get_mapped_doc(args.doctype, source_name, {
        args.doctype: {
			"doctype": "Payment Gateway Request",
			# "field_map": {
			# 	"reference_doctype": "doctype",
			# 	"reference_name": "name",
			# 	"amount":"grand_total",
			# 	"customer":"customer",
			# }
		}
    },
	target_doc,
	set_missing_values,
	ignore_permissions=True,
	)
	print(doc, target_doc)
	return doc
