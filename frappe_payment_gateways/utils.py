import frappe
from frappe import _


@frappe.whitelist()
def get_customer_contact(customer):
    """
    Get customer emails and phone numbers send back to sales invoice frontend
    """
    print(customer)
    contact_data = frappe._dict({})
    if frappe.db.exists("Customer", {'name':customer}):
        customer_doc = frappe.get_doc("Customer", customer)
        if customer_doc.customer_primary_contact:
            contact = frappe.get_doc("Contact", customer_doc.customer_primary_contact)
            if contact.email_ids:
                contact_data.emails = [i.email_id for i in contact.email_ids]
            if contact.phone_nos:
                contact_data.phone_nos = [i.phone for i in contact.phone_nos]
    if not (contact_data.phone_nos or contact_data.email_id):
        return False
    return contact_data

@frappe.whitelist()
def initiate_link(docname, recipient, channel, gateway):
    """
        Send the payment links
    """
    print(docname, recipient, channel, gateway)
    doc = frappe.get_doc("Sales Invoice", docname)
    if channel=='Email':
        email_template = frappe.get_doc("Email Template", "Send Payment Link Via Email")
        frappe.sendmail(
            recipients=[recipient],
            subject=frappe._(f"Payment link for {docname}"),
            message=email_template,
            attachments=[frappe.attach_print(doc.doctype, doc.name, file_name=doc.name)],
        )