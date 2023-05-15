// Copyright (c) 2023, Anthony C. Emmanuel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Gateway Request', {
	refresh: function(frm) {
		frm.trigger('set_values');
	},
	set_values: function(frm){
		// set date
		if (!frm.doc.request_date){
			frm.set_value('request_date', frappe.datetime.get_today());
		}
	},
	reference_name: function(frm){
		// get amount if exist
		frm.call('get_amount', {doc:frm.doc}).then(res=>{
			if (res.message>0){
				frm.set_value('amount', res.message);
			}
		})
	}
});
