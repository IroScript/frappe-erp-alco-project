# MASTER RULEBOOK: FRAPPE FRAMEWORK & ERPNEXT VERSION 16+ ONLY (`gemini.md`)

> 🚨 **CRITICAL MANDATE FOR AI CODING ASSISTANTS & DEVELOPERS** 🚨
> 
> 1. **STRICT VERSION LOCK:** You must **ONLY** use **Frappe Framework Version 16+** and **ERPNext Version 16+**.
> 2. **NO OLD VERSION CODE (STRICTLY PROHIBITED):** Under NO circumstances are you allowed to write code for **Version 15 (v15)**, **Version 14 (v14)**, **Version 13 (v13)**, or **Version 12 (v12)**. Writing any legacy syntax, deprecated functions, or v15/older APIs is an absolute failure.
> 3. **MANDATORY DOCUMENTATION & SOURCE VERIFICATION:** Before writing any line of code, you **MUST** inspect and cross-verify the syntax against official **Frappe / ERPNext Version 16 (v16)** documentation and local v16 source files in `frappe-framework-v16/` and `erpnext-v16/`.

---

## 1. Installation & Environment Overview (Latest Version 16)

### 1.1 Local Repositories & Docker Integration
- **Frappe Framework v16:** Cloned in `frappe-framework-v16/` (branch: `develop` / v16).
- **ERPNext v16:** Cloned in `erpnext-v16/` (branch: `develop` / v16).
- **Docker Desktop:** Running and configured for containerized execution.

### 1.2 Bench Execution Commands (v16)
```bash
# Initialize bench with Frappe Framework Version 16
bench init frappe-bench --frappe-branch develop

# Create site and install ERPNext Version 16
cd frappe-bench
bench new-site site1.local
bench get-app erpnext --branch develop
bench install-app erpnext site1.local
bench start
```

---

## 2. Strict Coding Directives for AI Assistant

### ❌ STRICTLY FORBIDDEN (OLD / LEGACY VERSION CODE - DO NOT WRITE):
- 🛑 **NO Version 15 (v15) Syntax or APIs:** Do NOT write v15 or older code patterns.
- 🛑 **NO Deprecated DB Calls:** Do NOT write raw unparameterized SQL queries or old positional `frappe.db.get_value` calls without keyword arguments.
- 🛑 **NO Legacy JS Syntax:** Do NOT use `cur_frm`, `cur_dialog`, global `$` jQuery DOM mutations, or legacy Desk v12-v15 handlers.
- 🛑 **NO Outdated Hooks:** Do NOT use deprecated hook event signatures from v15 or earlier.

### ✅ MANDATORY (VERSION 16+ STANDARDS ONLY):
- ✨ **Python Query Builder (`frappe.qb`):** Always write database queries using PyPika Query Builder (`frappe.qb.from_`).
- ✨ **Strict Type Annotations:** Backend functions must include explicit Python type hints (e.g. `customer_name: str -> list[dict]`).
- ✨ **Modern Desk & Dialog APIs:** Use `frappe.ui.Dialog`, `frm.add_custom_button`, and fluid responsive components.
- ✨ **Security & Whitelisting:** Mandatory `@frappe.whitelist()` with permission validations.

---

## 3. Version 16 Reference Implementations

### 3.1 Modern Python Backend (v16 Standard)
```python
import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType

class CustomV16Feature(Document):
    def validate(self):
        """v16 Document validation lifecycle"""
        self.recalculate_totals()
    
    def recalculate_totals(self):
        total = 0.0
        for row in self.items:
            row.amount = row.qty * row.rate
            total += row.amount
        self.grand_total = total

@frappe.whitelist()
def fetch_v16_sales_data(customer_code: str) -> list[dict]:
    """Modern v16 Query Builder API implementation"""
    if not customer_code:
        frappe.throw(frappe._("Customer Code is required."))
    
    SalesOrder = DocType("Sales Order")
    
    query = (
        frappe.qb.from_(SalesOrder)
        .select(SalesOrder.name, SalesOrder.transaction_date, SalesOrder.grand_total, SalesOrder.status)
        .where(SalesOrder.customer == customer_code)
        .where(SalesOrder.docstatus == 1)
        .orderby(SalesOrder.transaction_date, order=frappe.qb.desc)
        .limit(10)
    )
    
    return query.run(as_dict=True)
```

### 3.2 Modern JavaScript Frontend (v16 Standard)
```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('v16 Quick Action'), () => {
                frm.events.show_v16_dialog(frm);
            }, __('Actions'));
        }
    },

    show_v16_dialog(frm) {
        const dialog = new frappe.ui.Dialog({
            title: __('Version 16 Action Panel'),
            fields: [
                {
                    label: __('Remarks'),
                    fieldname: 'remarks',
                    fieldtype: 'Small Text',
                    reqd: 1
                }
            ],
            primary_action_label: __('Submit'),
            primary_action(values) {
                frappe.call({
                    method: 'custom_app.api.process_v16_remarks',
                    args: {
                        docname: frm.doc.name,
                        remarks: values.remarks
                    },
                    freeze: true,
                    freeze_message: __('Processing in v16 Engine...'),
                    callback(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('Operation completed successfully!'));
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

---

## 4. Mandatory User Git Rules & Workflow Controls

1. **NO UNPROMPTED GIT PUSH:** The AI assistant must **NEVER** execute `git push` on its own. The decision to push belongs solely to the user when they command `'git push'`.
2. **PRESERVE COMMIT HISTORY:** Never delete old commit messages or rewrite git history (`git reset --hard` or `git push --force` are strictly forbidden).
3. **200% CLOUD VERIFICATION:**
   ```powershell
   git ls-remote origin main; git log --oneline -1
   # If remote hash matches local HEAD hash, push is 200% confirmed in cloud.
   ```
