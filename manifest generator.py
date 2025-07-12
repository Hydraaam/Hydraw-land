import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import uuid
import json

# لیست ماژول‌ها
MODULE_CHOICES = [
    "data", "resources", "client_data", "scripting",
    "world_template", "skin_pack", "interface",
    "texture_data", "game_test", "chemistry", "feature_rules"
]

def new_uuid():
    return str(uuid.uuid4())

def build_manifest(name, description, version, selected_modules):
    version_list = [int(x) for x in version.split(".")]
    header_uuid = new_uuid()

    manifest = {
        "format_version": 2,
        "header": {
            "name": name,
            "description": description,
            "uuid": header_uuid,
            "version": version_list,
            "min_engine_version": [1, 20, 0]
        },
        "modules": []
    }

    for mod in selected_modules:
        manifest["modules"].append({
            "type": mod,
            "uuid": new_uuid(),
            "version": version_list
        })

    return manifest

def save_manifest(manifest):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="ذخیره فایل manifest"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("موفقیت", f"فایل با موفقیت ذخیره شد:\n{file_path}")

def generate_manifest():
    name = entry_name.get().strip()
    description = entry_description.get().strip()
    version = entry_version.get().strip()
    selected = [mod for mod, var in module_vars.items() if var.get()]

    if not name or not description or not version:
        messagebox.showerror("خطا", "لطفاً تمام فیلدها را پر کن!")
        return
    if not selected:
        messagebox.showerror("خطا", "حداقل یک ماژول را انتخاب کن!")
        return

    try:
        manifest = build_manifest(name, description, version, selected)
        save_manifest(manifest)
    except Exception as e:
        messagebox.showerror("خطا", f"مشکلی پیش آمد:\n{e}")

# رابط کاربری
root = tk.Tk()
root.title("🎮 ساخت فایل Manifest برای Minecraft Bedrock")
root.geometry("500x600")
root.resizable(False, False)

# فریم اطلاعات پک
frame_info = ttk.LabelFrame(root, text="📦 اطلاعات پکت")
frame_info.pack(padx=15, pady=10, fill="x")

ttk.Label(frame_info, text="📝 نام پک:").pack(anchor="w", padx=10, pady=2)
entry_name = ttk.Entry(frame_info)
entry_name.pack(fill="x", padx=10)

ttk.Label(frame_info, text="💬 توضیح پک:").pack(anchor="w", padx=10, pady=2)
entry_description = ttk.Entry(frame_info)
entry_description.pack(fill="x", padx=10)

ttk.Label(frame_info, text="🧮 نسخه (مثلاً 1.0.0):").pack(anchor="w", padx=10, pady=2)
entry_version = ttk.Entry(frame_info)
entry_version.insert(0, "1.0.0")
entry_version.pack(fill="x", padx=10)

# فریم انتخاب ماژول‌ها
frame_modules = ttk.LabelFrame(root, text="🧩 ماژول‌هایی که می‌خوای فعال باشن:")
frame_modules.pack(padx=15, pady=10, fill="both", expand=True)

module_vars = {}
for mod in MODULE_CHOICES:
    var = tk.BooleanVar(value=(mod == "data"))  # پیش‌فرض data فعاله
    chk = ttk.Checkbutton(frame_modules, text=mod, variable=var)
    chk.pack(anchor="w", padx=10)
    module_vars[mod] = var

# دکمه ساخت فایل
btn_create = ttk.Button(root, text="🔨 ساخت فایل manifest.json", command=generate_manifest)
btn_create.pack(pady=20)

root.mainloop()
