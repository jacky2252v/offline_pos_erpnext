// Copyright (c) 2024, offline and contributors
// For license information, please see license.txt

frappe.ui.form.on('Desktop POS Setting', {
	refresh: function(frm) {
		frm.add_custom_button(__("After Install"), function(){
			frm.call({
				method: "offline_pos_erpnext.install.after_install",
				callback: function (r) {
					if (!r.exc) {
						frappe.msgprint("Bench executed successfully!!")
					}
				}
			})			
		  });
	}
});
