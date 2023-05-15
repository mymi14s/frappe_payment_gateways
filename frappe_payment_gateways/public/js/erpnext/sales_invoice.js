// Copyright (c) 2023, Anthony Emmanuel
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
        // show payment button if invoice status is unpaid
        $('button[data-doctype="Payment Gateway Request"]').hide();
        if (frm.doc.docstatus==1 && frm.doc.status!='Paid'){
            frm.trigger('create_payment_request');
        }
	},
    create_payment_request: (frm)=>{
        // check for contact
        frappe.call({
            method: "frappe_payment_gateways.utils.get_customer_contact",
            args: {customer:frm.doc.customer},
            callback: function(res) {
                // if contact exits
                console.log(res.message)
                if (res.message){
                    console.log(res.message)
                    if (res.message.emails){
                        frm.add_custom_button('Create Payment Request', () => {
                            // Payment request
                            frappe.new_doc("Payment Gateway Request",{
                                "reference_doctype":frm.doc.doctype,
                                "reference_name":frm.doc.name,
                                "customer":frm.doc.customer,
                                "email":res.message.emails,
                                "amount":frm.doc.grand_total,
                                "cost_center":frm.doc.cost_center,
                            })
                        });    
                    } else {
                        frm.add_custom_button('Create Payment Request', () => {
                            // Payment request
                            frappe.new_doc("Payment Gateway Request",{
                                "reference_doctype":frm.doc.doctype,
                                "reference_name":frm.doc.name,
                                "customer":frm.doc.customer,
                                "amount":frm.doc.grand_total,
                                "cost_center":frm.doc.cost_center,
                            })
                        }); 
                    }
                    
                } else {
                    console.log('here')
                    frm.add_custom_button('Create Payment Request', () => {
                        // Payment request
                        frappe.model.open_mapped_doc({
                            method: "frappe_payment_gateways.frappe_payment_gateways.doctype.payment_gateway_request.payment_gateway_request.make_payment_gateway_request",
                            frm:frm,
                            args: {doctype:frm.doc.doctype, docname:frm.doc.name}
                        })
                        // frappe.new_doc("Payment Gateway Request",{
                        //     "reference_doctype":frm.doc.doctype,
                        //     "reference_name":frm.doc.name,
                        //     "customer":frm.doc.customer,
                        //     "amount":frm.doc.grand_total,
                        //     "cost_center":frm.doc.cost_center,
                        // }).save()
                    });
                }
                document.querySelector('[data-label="Create%20Payment%20Request"]').style.backgroundColor = 'yellow';
                document.querySelector('[data-label="Create%20Payment%20Request"]').style.color = 'black';
                    
            }
        });
        
        
    },
    
    
});


const initiate_link = (frm, res, channel)=>{
        // send payment link for Email
        let d = new frappe.ui.Dialog({
            title: 'Select Gateway and Contact',
            fields: [
                {
                    label: 'Gateway',
                    fieldname: 'gateway',
                    fieldtype: 'Select',
                    options: res.gateways,
                    reqd: 1,
                    default: res.gateways[0]
                },
                {
                    label: `Recipient ${channel=='Email' ? 'Email' : 'Phone'}`,
                    fieldname: 'recipient',
                    fieldtype: 'Select',
                    options: channel=='Email' ? res.emails : res.phone_nos,
                    reqd: 1,
                    default: channel=='Email' ? res.emails[0] : res.phone_nos[0]
                }
            ],
            primary_action_label: 'Send',
            secondary_action_label: 'Cancel',
            primary_action(values) {
                // send to backend
                values.channel = channel
                values.docname = frm.doc.name
                frappe.call({
                    method: "ngn_online_payment.utils.initiate_link",
                    type: "POST",
                    args: values,
                    callback: function(r) {},
                    freeze: true,
                    freeze_message: `Sending payment link via ${channel}`,
                    async: true
                });
                
                d.hide();
            },
            secondary_action(values){
                d.hide();
            }
        });
        
        d.show();
}