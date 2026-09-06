# 📖 ERPNext Version 16+ এবং Frappe Framework Version 16+ রান করার পূর্ণাঙ্গ গাইড

---

## ❓ ১. কেন সরাসরি উইন্ডোজে `bench start` চলে না এবং ডকার (Docker) কেন প্রয়োজন?

* **Frappe Framework ও ERPNext-এর আর্কিটেকচার:** Frappe এবং ERPNext মূলত লিনাক্স (Linux / POSIX) আর্কিটেকচারের জন্য তৈরি। এর বিভিন্ন গুরুত্বপূর্ণ ব্যাকএন্ড কম্পোনেন্ট (যেমন: Redis Server, MariaDB Database Sockets, Gunicorn Server, RQ Workers, Socket.io) উইন্ডোজের সাধারণ CMD বা PowerShell-এ সরাসরি সাপোর্ট করে না।
* **ডকার (Docker) কী কাজ করে:** উইন্ডোজ কম্পিউটারে লিনাক্সের একটি বিচ্ছিন্ন ও সুরক্ষিত পরিবেশ (Container) তৈরি করে দেয়। এর ফলে কোনো ডিপেন্ডেন্সি জটিলতা ছাড়াই Frappe ও ERPNext v16 নির্বিঘ্নে চলতে পারে।
* **ডকার টার্মিনাল (Docker Terminal) কী:** `docker exec -it ... bash` কমান্ড দিলে আপনি সরাসরি ডকার কন্টেইনারের লিনাক্স টার্মিনালে প্রবেশ করবেন। সেখানে আপনি লিনাক্সের মতো সরাসরি `bench start` বা যেকোনো bench কমান্ড চালাতে পারবেন।

---

## 🚀 ২. কীভাবে রান করবেন? (২টি সহজ পদ্ধতি)

---

### 🔹 পদ্ধতি ১: সরাসরি ডকার টার্মিনালে ঢুকে `bench start` চালানো (Docker Terminal Method)

আপনি যদি সাধারণ লিনাক্স মেশিনের মতো টার্মিনালে ঢুকে কমান্ড দিতে চান:

#### ধাপ ১: উইন্ডোজ PowerShell বা Terminal ওপেন করুন এবং কন্টেইনারগুলো স্টার্ট করুন:
```powershell
docker start mariadb_db redis_db erpnext_v16_container
```

#### ধাপ ২: ডকার কন্টেইনারের টার্মিনালে প্রবেশ করুন (Docker Terminal Entry):
```powershell
docker exec -it -u frappe -w /home/frappe/frappe-bench erpnext_v16_container bash
```
> 💡 *এই কমান্ড দেওয়ার পর আপনার টার্মিনাল প্রম্পট পরিবর্তিত হয়ে `frappe@...:~/frappe-bench$` হয়ে যাবে (এটিই ডকার টার্মিনাল)।*

#### ধাপ ৩: এবার সরাসরি `bench start` বা `bench serve` কমান্ড দিন:
```bash
bench start
```
*(অথবা আপনি চাইলে `bench serve --host 0.0.0.0 --port 8000` দিতে পারেন)*

> ⚠️ **যদি `Port 8000 is in use by another program` এরর আসে:**
> এর মানে হলো পূর্বে ব্যাকগ্রাউন্ডে সার্ভার অলরেডি চালু করা ছিল। টার্মিনালে নিচের কমান্ডটি দিয়ে পোর্ট ফ্রি করে নিন:
> ```bash
> pkill -f "frappe serve"
> ```
> এরপর আবার `bench start` দিন!

#### ধাপ ৪: ডকার টার্মিনাল থেকে বের হতে:
কীবোর্ডে `Ctrl + C` চাপুন সার্ভার থামাতে, অথবা অন্য ট্যাবে কাজ শেষ হলে `exit` টাইপ করে এন্টার দিন।

---

### 🔹 পদ্ধতি ২: উইন্ডোজ PowerShell থেকেই এক ক্লিকে ব্যাকগ্রাউন্ডে চালানো (One-Line Execution)

ডকার টার্মিনালে না ঢুকে সরাসরি উইন্ডোজ PowerShell থেকেই সার্ভিস রান করতে পারেন:

#### ধাপ ১: কন্টেইনার চালু করা:
```powershell
docker start mariadb_db redis_db erpnext_v16_container
```

#### ধাপ ২: ব্যাকগ্রাউন্ডে Frappe v16 সার্ভার চালু করা:
```powershell
docker exec -d -w /home/frappe/frappe-bench erpnext_v16_container bench serve --host 0.0.0.0 --port 8000
```

---

## 🌐 ৩. ব্রাউজারে সাইট ওপেন এবং লগইন তথ্য

সার্ভার চালু হওয়ার পর আপনার পছন্দের ব্রাউজারে নিচের ঠিকানায় যান:

* **URL:** [http://localhost:8000](http://localhost:8000)
* **ইউজারনেম (Username):** `Administrator`
* **পাসওয়ার্ড (Password):** `admin`

---

## 🛠️ ৪. অন্যান্য প্রয়োজনীয় কমান্ডসমূহ (Useful Commands Reference)

| কাজের বিবরণ | PowerShell থেকে সরাসরি কমান্ড |
| :--- | :--- |
| **ডাটাবেস মাইগ্রেশন (Migrate)** | `docker exec -w /home/frappe/frappe-bench erpnext_v16_container bench --site test.local migrate` |
| **ফ্রন্টএন্ড এসেটস বিল্ড (Build)** | `docker exec -w /home/frappe/frappe-bench erpnext_v16_container bench build` |
| **ক্যাশে ক্লিয়ার (Clear Cache)** | `docker exec -w /home/frappe/frappe-bench erpnext_v16_container bench --site test.local clear-cache` |
| **কন্টেইনারসমূহ বন্ধ করা (Stop)** | `docker stop erpnext_v16_container redis_db mariadb_db` |

---

## 📂 ফাইল পাথ রেফারেন্স:
* মাস্টার রুলবুক: `C:\Users\Irak\Desktop\frappeERP-Next\gemini.md`
* সিস্টেম ইন্সট্রাকশন: `C:\Users\Irak\Desktop\frappeERP-Next\AGENTS.md`
* প্রজেক্ট ডিরেক্টরি: `C:\Users\Irak\Desktop\frappeERP-Next`
