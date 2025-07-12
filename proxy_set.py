import tkinter as tk
from tkinter import messagebox
import os
import ctypes

def set_proxy():
    http = http_entry.get()
    https = https_entry.get()
    
    if not http or not https:
        messagebox.showwarning("خطا", "لطفاً هر دو فیلد HTTP و HTTPS را پر کن!")
        return
    
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showerror("دسترسی", "اسکریپت باید با دسترسی ادمین اجرا شود!")
        return

    command = f'netsh winhttp set proxy proxy-server="http={http};https={https}"'
    result = os.system(command)

    if result == 0:
        messagebox.showinfo("انجام شد", "پروکسی با موفقیت تنظیم شد ✅")
    else:
        messagebox.showerror("خطا", "تنظیم پروکسی انجام نشد ❌")

def reset_proxy():
    os.system("netsh winhttp reset proxy")
    messagebox.showinfo("ریست شد", "پروکسی ریست شد 🔄")

# پنجره
root = tk.Tk()
root.title("made by hydraw")
root.geometry("400x250")
root.resizable(False, False)

# استایل ساده
root.configure(bg="#1e1e1e")
label_style = {"fg": "white", "bg": "#1e1e1e", "font": ("Segoe UI", 10)}
entry_style = {"bg": "#333333", "fg": "white", "insertbackground": "white", "font": ("Segoe UI", 10)}

# لیبل‌ها و ورودی‌ها
tk.Label(root, text="آدرس HTTP:", **label_style).pack(pady=(20, 0))
http_entry = tk.Entry(root, **entry_style, width=40)
http_entry.pack()

tk.Label(root, text="آدرس HTTPS:", **label_style).pack(pady=(10, 0))
https_entry = tk.Entry(root, **entry_style, width=40)
https_entry.pack()

# دکمه‌ها
tk.Button(root, text="تنظیم پروکسی", command=set_proxy, bg="#00b894", fg="white", width=25).pack(pady=15)
tk.Button(root, text="ریست پروکسی", command=reset_proxy, bg="#d63031", fg="white", width=25).pack()

# استارت برنامه
root.mainloop()
