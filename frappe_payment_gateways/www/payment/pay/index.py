import frappe, json, requests



@frappe.whitelist(allow_guest=True)
def get_payment_request(id):
    id = frappe.form_dict.id
    if not id:
        return {'error':"Invalid payment link."}
    payment_data = frappe.db.get_value(
        "Payment Gateway Request", {
            "name":id, 
            # "docstatus":0, 
            # "status":["!=", "Paid"]
        }, "*")
    if not payment_data:
        return {'error':"Invalid payment link."}
    if payment_data.status=='Paid':
        return {'error':"Payment has already been made."}
    payment_data.public_key = frappe.db.get_value(
        "Payment Gateway Integration Settings",
        {'enabled':1, 'gateway':payment_data.gateway},
        ["public_key"])
    return {'data':payment_data}

@frappe.whitelist(allow_guest=True)
def verify_transaction(transaction):
    frappe.enqueue(queue_verify_transaction, transaction=transaction)

def queue_verify_transaction(transaction):
    # check the authenticity of transaction
    try:
        transaction = frappe._dict(json.loads(transaction))
        if transaction.gateway=='Paystack':
            secret_key = frappe.get_doc(
                "Payment Gateway Integration Settings",
                {'enabled':1, 'gateway':transaction.gateway}
            ).get_secret_key()
            headers = {"Authorization": f"Bearer {secret_key}"}
            req = requests.get(
                f"https://api.paystack.co/transaction/verify/{transaction.reference}",
                headers=headers, timeout=10
            )
            if req.status_code in [200, 201]:
                response = frappe._dict(req.json())
                data = frappe._dict(response.data)
                metadata = frappe._dict(data.metadata)
                frappe.get_doc({
                    'doctype':"Payment Gateway Log",
                    'amount':data.amount/100,
                    'currency':data.currency,
                    'message':response.message,
                    'status':data.status,
                    'payment_gateway_request': metadata.log_id,
                    'reference': data.reference,
                    'reference_doctype': metadata.reference_doctype,
                    'reference_name': metadata.reference_name,
                    'transaction_id': data.id,
                    'data': response
                }).insert(ignore_permissions=True)
            else:
                # log error
                frappe.log_error(str(req.reason), 'Verify Transaction')
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Verify Transaction')



@frappe.whitelist(allow_guest=True)
def paystack_webhook(**kwargs):
    """
        End point where payment gateway sends payment info.
    """
    try:
        data = frappe._dict(frappe.form_dict.data)
        if not (frappe.db.exists("Payment Gateway Request", {"name":data.reference})):
            secret_key = frappe.get_doc(
                "Payment Gateway Integration Settings",
                {'enabled':1, 'gateway':'Paystack'}
            ).get_secret_key()
            headers = {"Authorization": f"Bearer {secret_key}"}
            req = requests.get(
                f"https://api.paystack.co/transaction/verify/{data.reference}",
                headers=headers, timeout=10
            )
            if req.status_code in [200, 201]:
                response = frappe._dict(req.json())
                data = frappe._dict(response.data)
                metadata = frappe._dict(data.metadata)
                frappe.get_doc({
                    'doctype':"Payment Gateway Log",
                    'amount':data.amount/100,
                    'currency':data.currency,
                    'message':response.message,
                    'status':data.status,
                    'payment_gateway_request': metadata.log_id,
                    'reference': data.reference,
                    'reference_doctype': metadata.reference_doctype,
                    'reference_name': metadata.reference_name,
                    'transaction_id': data.id,
                    'data': response
                }).insert(ignore_permissions=True)
            else:
                # log error
                frappe.log_error(str(req.reason), 'Verify Transaction')
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Verify Transaction')

