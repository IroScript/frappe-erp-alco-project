frappe.ui.form.on("Alco Field Order", {
    refresh(frm) {
        // Print Invoice Action
        if (!frm.is_new()) {
            frm.add_custom_button(__("Print Official Invoice"), () => {
                frm.print_doc();
            }, __("Actions"));

            // Open Web Storefront
            frm.add_custom_button(__("Web Storefront"), () => {
                window.open("/alco-order", "_blank");
            }, __("Actions"));
        }

        // ERPNext Sales Order Integration
        if (frm.doc.docstatus === 1 && !frm.doc.erpnext_sales_order) {
            frm.add_custom_button(__("Create ERPNext Sales Order"), () => {
                frappe.confirm(
                    __("Are you sure you want to create an ERPNext Sales Order from this Field Order?"),
                    () => {
                        frappe.call({
                            method: "alco_ecommerce.api.create_erpnext_sales_order",
                            args: {
                                field_order_name: frm.doc.name
                            },
                            freeze: true,
                            freeze_message: __("Creating ERPNext Sales Order..."),
                            callback(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint({
                                        title: __("Success"),
                                        indicator: "green",
                                        message: __("ERPNext Sales Order <b>{0}</b> created successfully!", [r.message.sales_order])
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __("ERPNext Integration"));
        } else if (frm.doc.erpnext_sales_order) {
            frm.add_custom_button(__("View Sales Order: {0}", [frm.doc.erpnext_sales_order]), () => {
                frappe.set_route("Form", "Sales Order", frm.doc.erpnext_sales_order);
            }, __("ERPNext Integration"));
        }
    },

    validate(frm) {
        frm.events.recalculate_totals(frm);
    },

    recalculate_totals(frm) {
        let total = 0.0;
        (frm.doc.items || []).forEach(row => {
            row.amount = flt(row.qty) * flt(row.rate);
            total += row.amount;
        });
        frm.set_value("grand_total", total);
    }
});

frappe.ui.form.on("Alco Field Order Item", {
    qty(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", flt(row.qty) * flt(row.rate));
        frm.events.recalculate_totals(frm);
    },
    rate(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", flt(row.qty) * flt(row.rate));
        frm.events.recalculate_totals(frm);
    },
    items_remove(frm) {
        frm.events.recalculate_totals(frm);
    }
});
