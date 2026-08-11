# Frappe Framework & ERPNext Latest Version Master Rulebook & Guidelines (`gemini.md`)

> **গুরুত্বপূর্ণ নির্দেশিকা (Master Directive):**
> এই প্রজেক্টে **Frappe Framework** এবং **Frappe ERPNext**-এর **সর্বশেষ ভার্সন (Latest Version - Version 16+)** ইনস্টল এবং ব্যবহার করা আবশ্যক।
> **কোনো অবস্থাতেই কোনো পুরাতন ভার্সন (Old/Deprecated Version - v12, v13, v14 বা পুরনো API/Syntax) এর কোড লেখা যাবে না।** সকল কোড, কাস্টম মডিউল, হুকস এবং সিনট্যাক্স অবশ্যই Frappe & ERPNext Latest Version Standard অনুযায়ী লিখতে হবে।

---

## 1. ইনস্টলেশন এবং সেটআপ নির্দেশিকা (Installation & Setup Guide)

### ১.১ Frappe Bench ও পরিবেশ প্রস্তুতি (Bench Setup)
সর্বশেষ Frappe Framework ও ERPNext রান এবং ডেভেলপ করার জন্য Bench CLI ও Docker/WSL এনভায়রনমেন্ট প্রয়োজন:
```powershell
# Pip এর মাধ্যমে frappe-bench ইনস্টল
pip install frappe-bench

# Frappe Bench সংস্করণ পরীক্ষা
bench --version
```

### ১.২ সর্বশেষ ভার্সন দিয়ে Bench ইনিশিয়ালাইজেশন (Initialize Bench with Latest Version)
```bash
# Frappe Framework এর সর্বশেষ (Version 16 / develop) সংস্করণ সহ Bench তৈরি
bench init frappe-bench --frappe-branch develop

# প্রজেক্ট ডিরেক্টরিতে প্রবেশ
cd frappe-bench

# নতুন লোকাল সাইট তৈরি
bench new-site site1.local
```

### ১.৩ ERPNext এর সর্বশেষ ভার্সন ইনস্টলেশন (Get & Install Latest ERPNext)
```bash
# ERPNext এর সর্বশেষ ভার্সন ডাউনলোড
bench get-app erpnext --branch develop

# লোকাল সাইটে ERPNext ইনস্টল
bench install-app erpnext site1.local

# ডেভেলপমেন্ট সার্ভার চালু
bench start
```

---

## 2. কঠোর কোডিং স্ট্যান্ডার্ডস (Strict Coding Directives - Latest Version Only)

### ❌ বর্জনীয় (DO NOT USE - Legacy / Old Version Code):
- **Old Syntax:** `frappe.db.get_value("DocType", "name", "fieldname")` (Positional args positional list index without dict/kwargs).
- **Old JS Syntax:** `cur_frm`, `cur_dialog`, direct DOM manipulation with jQuery selectors.
- **Old API Call:** Unsanitized raw SQL queries using direct string interpolation `frappe.db.sql(f"SELECT * FROM tabDoc WHERE name='{val}'")`.
- **Deprecated Hooks:** Old hook names from v12/v13/v14.

### ✅ গ্রহণীয় (ALWAYS USE - Latest Version v16+ Standard):
- **Python Query Builder (`frappe.qb` PyPika):** ডাটাবেজ কোয়েরির জন্য সবসময় Query Builder ব্যবহার করুন।
- **Typed & Keyword Arguments:** Python ORM মেথডে স্পষ্ট কি-ওয়ার্ড আর্গুমেন্টস এবং টাইপ অ্যানোটেশন।
- **Modern Form Controllers:** Form lifecycle event handling standards.
- **Strict Permission & Whitelisting:** `@frappe.whitelist(allow_guest=False)` সহ কঠোর সিকিউরিটি চেকিং।

---

## 3. আধুনিক কোড উদাহরণ (Modern Code Reference Examples)

### ৩.১ Modern Python Backend Code (v16 Standard)
```python
import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType

class CustomCustomerRequirement(Document):
    def validate(self):
        """সর্বশেষ ভার্সন অনুযায়ী ডকুমেন্ট ভ্যালিডেশন"""
        self.calculate_totals()
    
    def calculate_totals(self):
        total = 0.0
        for item in self.items:
            item.amount = item.qty * item.rate
            total += item.amount
        self.total_amount = total

@frappe.whitelist()
def get_latest_sales_orders(customer_name: str) -> list[dict]:
    """frappe.qb (Query Builder) ব্যবহার করে আধুনিক ও নিরাপদ কোয়েরি"""
    if not customer_name:
        frappe.throw(frappe._("কাস্টমারের নাম প্রদান করা বাধ্যতামূলক।"))
    
    SalesOrder = DocType("Sales Order")
    
    query = (
        frappe.qb.from_(SalesOrder)
        .select(SalesOrder.name, SalesOrder.transaction_date, SalesOrder.grand_total, SalesOrder.status)
        .where(SalesOrder.customer == customer_name)
        .where(SalesOrder.docstatus == 1)
        .orderby(SalesOrder.transaction_date, order=frappe.qb.desc)
        .limit(10)
    )
    
    return query.run(as_dict=True)
```

### ৩.২ Modern JavaScript Frontend Code (v16 Standard)
```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // আধুনিক বোতাম যোগ করার নিয়ম
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('কাস্টম অ্যাকশন সূচি'), () => {
                frm.events.trigger_custom_dialog(frm);
            }, __('কার্যাবলী'));
        }
    },

    trigger_custom_dialog(frm) {
        // আধুনিক Frappe Dialog API
        const dialog = new frappe.ui.Dialog({
            title: __('অতিরিক্ত তথ্য যোগ করুন'),
            fields: [
                {
                    label: __('মন্তব্য (Notes)'),
                    fieldname: 'notes',
                    fieldtype: 'Small Text',
                    reqd: 1
                }
            ],
            primary_action_label: __('সংরক্ষণ করুন'),
            primary_action(values) {
                frappe.call({
                    method: 'your_app.api.save_notes',
                    args: {
                        sales_order: frm.doc.name,
                        notes: values.notes
                    },
                    freeze: true,
                    freeze_message: __('সংরক্ষণ করা হচ্ছে...'),
                    callback(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('সফলভাবে নিবন্ধিত হয়েছে!'));
                            dialog.hide();
                            frm.reload_doc();
                        }
                    }
                });
            }
        });
        dialog.show();
    }
});
```

### ৩.৩ Modern `hooks.py` Definition
```python
app_name = "custom_erp_extension"
app_title = "Custom ERP Extension"
app_publisher = "IroScript"
app_description = "Frappe Framework & ERPNext Latest Version Customizations"
app_email = "md.kamruzzamanirak@gmail.com"
app_license = "mit"

# Modern Document Events
doc_events = {
    "Sales Invoice": {
        "on_submit": "custom_erp_extension.api.on_sales_invoice_submit",
        "on_cancel": "custom_erp_extension.api.on_sales_invoice_cancel"
    }
}

# Modern Scheduler Events
scheduler_events = {
    "daily": [
        "custom_erp_extension.tasks.daily_cleanup"
    ]
}
```

---

## 4. গিট ও পুশ ভ্যালিডেশন নিয়মাবলী (Git & Cloud Verification Rules)

1. **ইউজারের নির্দেশ ছাড়া পুশ নয়:** ইউজার থেকে সরাসরি `'git push'` কমান্ড না পাওয়া পর্যন্ত নিজে থেকে কখনই Git push দেওয়া যাবে না।
2. **পুরানো কমিট ইতিহাস সংরক্ষণ:** কোনো পুরাতন commit ডিলিট বা ওভাররাইট করা সম্পূর্ণ নিষিদ্ধ (`git reset --hard` বা `git push --force` বর্জনীয়)।
3. **২০০% গিটহাব ক্লাউড ভ্যালিডেশন:**
   ```powershell
   git ls-remote origin main; git log --oneline -1
   # যদি দুটি Commit Hash হুবহু মিলে যায় তবে কোড ২০০% ক্লাউডে নিশ্চিত রয়েছে।
   ```

---

> **নোট:** এই `gemini.md` ফাইলটি প্রজেক্টের মাস্টার গাইডলাইন হিসেবে সংরক্ষিত। ডেভেলপমেন্টের প্রতিটি ধাপে এই গাইডলাইন মেনে চলতে হবে।
