# MANDATORY AGENT DIRECTIVES & SYSTEM INSTRUCTIONS (`AGENTS.md`)

> 🛑 **CRITICAL RULE FOR ALL AI CODING AGENTS & TOOLS** 🛑
> 
> You are operating inside a Frappe Framework and ERPNext workspace.
> You must strictly observe the following mandatory constraints without exception:

---

## SECTION 1: GLOBAL AGENT DIRECTIVES & SYSTEM RULES

1. **BEFORE EDITING CODE:** You MUST test and verify all code changes yourself before applying them. Code must not be applied until tests pass successfully.
2. **FORCEFUL EXECUTION & WORKFLOW INTEGRITY:** Execute exactly what the user requests, test and verify fulfillment, and ensure total user workflow remains perfectly intact.
3. **RESPONSE LANGUAGE:** Always reply using Bangla script (সর্বদা বাংলা লিপি ব্যবহার করে উত্তর দাও, কোনো বাংলিশ নয়।).
4. **USER SALUTATION:** Always call the user **"ইরাক ভাইয়া"** when responding.
5. **GIT PUSH RULES (STRICT USER CONTROL):**
   - NEVER make the decision to push on your own.
   - NEVER question the user's command to push.
   - The decision to push MUST always come from the user. When the user says `'git push'`, execute it immediately.
   - NEVER git push from yourself until explicitly commanded.
   - NEVER delete any old git commit or perform hard resets (`git reset --hard`).
   - ALWAYS verify 200% availability in GitHub cloud using `git ls-remote origin main` and `git log -1`.
6. **KAGGLE SCRIPT FORMATTING:** Always provide a plain text version of any Kaggle script to avoid indentation issues when copy-pasting.
7. **PROTECTED PROCESS (OpenRecall):**
   - NEVER kill, stop, or terminate the `run_openrecall.py` process or any process with "openrecall" in its name.
   - Path: `C:\Users\Irak\Desktop\AI_Agent\DigitalHistory\run_openrecall.py`.
   - Exclude OpenRecall from any process cleanup commands.
8. **COMPLETION NOTIFICATION:** Always inform the user that all tasks are done, cross-checked, and 200% verified.

---

## SECTION 2: ERPNEXT & FRAPPE FRAMEWORK MANDATORY DIRECTIVES (VERSION 16+ ONLY)

> 🚨 **STRICT VERSION LOCK FOR FRAPPE FRAMEWORK & ERPNEXT** 🚨

1. **VERSION 16+ ONLY:** You must ONLY generate, modify, or suggest code written for **Frappe Framework Version 16+** and **ERPNext Version 16+**.
2. **VERSION 15 & OLDER CODE IS STRICTLY PROHIBITED:** Under NO circumstances are you allowed to write code for **Version 15 (v15)**, Version 14 (v14), Version 13 (v13), or Version 12 (v12). Any attempt to output deprecated v15/older APIs, syntax, or patterns is completely invalid.
3. **ALWAYS INSPECT V16 DOCUMENTATION & SOURCE FIRST:** Before generating any Python, JavaScript, JSON, HTML, or configuration code, you **MUST inspect and verify the syntax against Version 16 (v16) documentation** and local v16 source code available in `frappe-framework-v16/` and `erpnext-v16/`.
4. **DO NOT GUESS API METHODS:** Verify exact class definitions, method signatures, hook definitions, and field names in v16 source code prior to implementation.
5. **PYTHON STANDARD:** Use Python 3.12+ features, strict typing annotations, and PyPika Query Builder (`frappe.qb`). Never use obsolete DB functions or raw unescaped SQL.
6. **JAVASCRIPT STANDARD:** Use modern Frappe Form Controller patterns (`frappe.ui.form.on`), `frappe.ui.Dialog`, and `frappe.call`. Never use deprecated `cur_frm` or `cur_dialog`.

---

## SECTION 3: FRONTEND UI/UX DIRECTIVES (MOBILE-FIRST MANDATE)

> 📱 **MOBILE FIRST PRIORITY FOR FRONTEND (UI/UX) ONLY** 📱

1. **MOBILE FIRST PRIORITY (FRONTEND ONLY):** ফ্রন্টএন্ডের UI/UX ডিজাইনে সর্বদা **Mobile is First Priority (মোবাইল ফার্স্ট)** বিবেচনা করতে হবে। সমস্ত লেআউট, প্রোডাক্ট কার্ড, টাচ ইন্টারঅ্যাকশন, ন্যাভিগেশন, টাইপোগ্রাফি এবং বাটন সবার আগে মোবাইল স্ক্রিনের জন্য সর্বোচ্চ অপ্টিমাইজড ও সুন্দর হতে হবে।
2. **DESKTOP RESPONSIVENESS:** মোবাইল ফার্স্ট হলেও ডেস্কটপ স্ক্রিনের জন্যও সবকিছু শতভাগ সুন্দর, রেসপনসিভ ও নিখুঁতভাবে কাজ করবে (ডেস্কটপের জন্যও কাজ করবে অবশ্যই)।
3. **PRODUCT CARD SINGLE COLUMN:** মোবাইল ডিভাইসে (স্মার্টফোন ও পোট্রেট ভিউ) প্রোডাক্ট কার্ড সর্বদা **Single Column (১টি কলাম)** বিশিষ্ট হবে, যেন প্রতি লাইনে একটি করে পূর্ণাঙ্গ কার্ড দৃশ্যমান থাকে এবং তথ্য ও বাটনসমূহ সহজেই পড়া ও ব্যবহার করা যায়।

---

> **Note to Agents:** This document is authoritative. Adhere to these instructions for all code generation in this project.
