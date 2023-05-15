// Copyright (c) 2023, Anthony C. Emmanuel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Gateway Log', {
	refresh: function(frm) {
		frm.disable_save()
		frm.disable_form();
	}
});
