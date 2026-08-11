# MANDATORY AGENT DIRECTIVES & SYSTEM INSTRUCTIONS (`AGENTS.md`)

> 🛑 **CRITICAL RULE FOR ALL AI CODING AGENTS & TOOLS** 🛑
> 
> You are operating inside a Frappe Framework and ERPNext workspace.
> You must strictly observe the following mandatory constraints without exception:
>
> 1. **VERSION 16+ ONLY:** You must ONLY generate, modify, or suggest code written for **Frappe Framework Version 16+** and **ERPNext Version 16+**.
> 2. **VERSION 15 & OLDER CODE IS STRICTLY PROHIBITED:** Under NO circumstances are you allowed to write code for **Version 15 (v15)**, Version 14 (v14), Version 13 (v13), or Version 12 (v12). Any attempt to output deprecated v15/older APIs, syntax, or patterns is invalid.
> 3. **ALWAYS CHECK V16 DOCUMENTATION FIRST:** Before generating any Python, JavaScript, JSON, HTML, or configuration code, you **MUST inspect and verify the syntax against Version 16 (v16) documentation** and local v16 source code available in `frappe-framework-v16/` and `erpnext-v16/`.

---

## 1. Agent Behavior & Inspection Rules

When fulfilling any user request:
- **Inspect `frappe-framework-v16/` and `erpnext-v16/`:** Search the local v16 codebase to verify exact class definitions, method signatures, hook definitions, and field names.
- **Do Not Guess API Methods:** Verify method signatures in v16 before calling them.
- **Python Standard:** Use Python 3.12+ features, strict typing annotations, and PyPika Query Builder (`frappe.qb`). Never use obsolete DB functions or raw unescaped SQL.
- **JavaScript Standard:** Use modern Frappe Form Controller patterns (`frappe.ui.form.on`), `frappe.ui.Dialog`, and `frappe.call`. Never use deprecated `cur_frm` or `cur_dialog`.

---

## 2. Mandatory User Git Rules

- **NEVER PUSH ON YOUR OWN:** Do NOT execute `git push` unless the user explicitly commands `'git push'`.
- **PRESERVE GIT HISTORY:** Never delete old commits or perform hard resets (`git reset --hard`).
- **VERIFY CLOUD AVAILABILITY:** Always check local commit hash against remote hash using `git ls-remote origin main` and `git log -1`.

---

> **Note to Agents:** This document is authoritative. Adhere to these instructions for all code generation in this project.
