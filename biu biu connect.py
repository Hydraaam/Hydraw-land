import tkinter as tk
from tkinter import messagebox
import winreg
import os

def set_proxy():
    ip = entry_ip.get()
    port = entry_port.get()

    if not ip or not port:
        messagebox.showerror("خطا", "لطفاً IP و پورت را وارد کن!")
        return

    proxy = f"{ip}:{port}"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy)
        winreg.CloseKey(key)
        os.system("ipconfig /flushdns")
        messagebox.showinfo("موفقیت", f"پروکسی با موفقیت تنظیم شد:\n{proxy}")
    except Exception as e:
        messagebox.showerror("ارور", str(e))

def disable_proxy():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        os.system("ipconfig /flushdns")
        messagebox.showinfo("پروکسی غیرفعال شد", "پروکسی با موفقیت خاموش شد!")
    except Exception as e:
        messagebox.showerror("ارور", str(e))

# رابط گرافیکی
root = tk.Tk()
root.title("🔌 BlueStacks Proxy Control")
root.geometry("350x250")
root.resizable(False, False)

tk.Label(root, text="🖥 IP بلو استکس:", font=("Arial", 10)).pack(pady=5)
entry_ip = tk.Entry(root, width=30)
entry_ip.pack()

tk.Label(root, text="📡 پورت پروکسی:", font=("Arial", 10)).pack(pady=5)
entry_port = tk.Entry(root, width=10)
entry_port.pack()

tk.Button(root, text="🌐 Connect", bg="green", fg="white", font=("Arial", 12),
          command=set_proxy).pack(pady=10)

tk.Button(root, text="🚫 Disconnect", bg="red", fg="white", font=("Arial", 12),
          command=disable_proxy).pack()

tk.Label(root, text="by Hydraw 😈", font=("Arial", 8)).pack(side="bottom", pady=5)

root.mainloop()
