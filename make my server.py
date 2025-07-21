# ادامه کد قبلی با تکمیل بخش manage_world — اکنون این بخش کامل شده است
# این نسخه نهایی کل برنامه است، با مدیریت وورلد بدون تغییر ظاهر یا سایر بخش‌ها

import os
import sys
import subprocess
import threading
import requests
import zipfile
import shutil
import socket

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox,
    QTextEdit, QHBoxLayout, QFileDialog, QLineEdit, QMessageBox, QInputDialog, QListWidget
)
from PyQt6.QtCore import Qt

SERVER_DIR = "bedrock_server"
SERVER_ZIP_PATH = os.path.join(SERVER_DIR, "server.zip")
DEFAULT_WORLD = os.path.join(SERVER_DIR, "world")
PLUGINS_DIR = os.path.join(SERVER_DIR, "plugins")
DEFAULT_PORT = 19132

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class BedrockServerManager(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.current_world = DEFAULT_WORLD
        self.setAcceptDrops(True)

        self.setWindowTitle("مدیریت سرور ماینکرفت بدراک")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""QWidget { background-color: #121212; color: #E0E0E0; font-family: Arial; font-size: 14px; }
            QPushButton { background-color: #333333; color: #E0E0E0; border: none; padding: 8px 15px; border-radius: 5px; }
            QPushButton:hover { background-color: #555555; }
            QComboBox, QTextEdit, QLineEdit { background-color: #222222; color: #E0E0E0; border-radius: 5px; padding: 5px; }""")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.ip_label = QLabel(f"IP: {get_local_ip()}    |    Port: {DEFAULT_PORT}")
        layout.addWidget(self.ip_label)

        h_layout = QHBoxLayout()
        self.download_btn = QPushButton("درگ کن فایل ZIP رو اینجا یا کلیک برای نصب سرور")
        self.download_btn.clicked.connect(self.browse_zip)
        h_layout.addWidget(self.download_btn)
        layout.addLayout(h_layout)

        h_layout2 = QHBoxLayout()
        self.start_btn = QPushButton("شروع سرور")
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setEnabled(False)
        h_layout2.addWidget(self.start_btn)

        self.stop_btn = QPushButton("توقف سرور")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setEnabled(False)
        h_layout2.addWidget(self.stop_btn)

        self.status_btn = QPushButton("وضعیت سرور")
        self.status_btn.clicked.connect(self.check_status)
        h_layout2.addWidget(self.status_btn)

        layout.addLayout(h_layout2)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        h_layout3 = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("دستور برای ارسال به سرور")
        h_layout3.addWidget(self.cmd_input)
        self.send_cmd_btn = QPushButton("ارسال دستور")
        self.send_cmd_btn.clicked.connect(self.send_command)
        self.send_cmd_btn.setEnabled(False)
        h_layout3.addWidget(self.send_cmd_btn)
        layout.addLayout(h_layout3)

        h_layout4 = QHBoxLayout()

        self.backup_btn = QPushButton("بکاپ از وورلد")
        self.backup_btn.clicked.connect(self.backup_world)
        h_layout4.addWidget(self.backup_btn)

        self.manage_world_btn = QPushButton("مدیریت وورلد")
        self.manage_world_btn.clicked.connect(self.manage_world)
        h_layout4.addWidget(self.manage_world_btn)

        self.install_plugin_btn = QPushButton("نصب پلاگین")
        self.install_plugin_btn.clicked.connect(self.install_plugin)
        h_layout4.addWidget(self.install_plugin_btn)

        self.edit_props_btn = QPushButton("ویرایش server.properties")
        self.edit_props_btn.clicked.connect(self.edit_server_properties)
        h_layout4.addWidget(self.edit_props_btn)

        layout.addLayout(h_layout4)

        self.setLayout(layout)

    def log(self, message):
        self.log_text.append(message)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().endswith(".zip"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".zip"):
                self.install_zip_server(file_path)

    def browse_zip(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل ZIP سرور", "", "Zip Files (*.zip)")
        if file_path:
            self.install_zip_server(file_path)

    def install_zip_server(self, zip_path):
        self.log("در حال نصب سرور از فایل ZIP...")
        if not os.path.exists(SERVER_DIR):
            os.makedirs(SERVER_DIR)
        try:
            for item in os.listdir(SERVER_DIR):
                item_path = os.path.join(SERVER_DIR, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            shutil.copy(zip_path, SERVER_ZIP_PATH)
            with zipfile.ZipFile(SERVER_ZIP_PATH, 'r') as zip_ref:
                zip_ref.extractall(SERVER_DIR)
            self.log("سرور با موفقیت نصب شد.")
            self.start_btn.setEnabled(True)
        except Exception as e:
            self.log(f"خطا در نصب سرور: {e}")

    def start_server(self):
        if self.process and self.process.poll() is None:
            self.log("سرور در حال اجراست!")
            return
        exe_name = "bedrock_server.exe" if os.name == 'nt' else "bedrock_server"
        exe_path = os.path.join(SERVER_DIR, exe_name)
        if not os.path.exists(exe_path):
            self.log("فایل اجرایی سرور پیدا نشد!")
            return
        self.log("در حال شروع سرور...")
        self.process = subprocess.Popen([exe_path], cwd=SERVER_DIR, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.send_cmd_btn.setEnabled(True)
        threading.Thread(target=self.read_output, daemon=True).start()

    def read_output(self):
        for line in self.process.stdout:
            self.log(line.strip())

    def stop_server(self):
        if self.process and self.process.poll() is None:
            self.log("در حال توقف سرور...")
            self.process.terminate()
            self.process.wait()
            self.log("سرور متوقف شد.")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.send_cmd_btn.setEnabled(False)
        else:
            self.log("سرور در حال اجرا نیست.")

    def check_status(self):
        if self.process and self.process.poll() is None:
            self.log("سرور در حال اجراست.")
        else:
            self.log("سرور متوقف است.")

    def send_command(self):
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(cmd + "\n")
                self.process.stdin.flush()
                self.log(f">>> {cmd}")
                self.cmd_input.clear()
            except Exception as e:
                self.log(f"ارسال دستور ناموفق بود: {e}")
        else:
            self.log("سرور در حال اجرا نیست.")

    def backup_world(self):
        if not os.path.exists(self.current_world):
            self.log("وورلد فعلی وجود ندارد.")
            return
        backup_name, ok = QInputDialog.getText(self, "بکاپ وورلد", "نام بکاپ:")
        if not ok or not backup_name:
            return
        try:
            shutil.make_archive(os.path.join(SERVER_DIR, backup_name), 'zip', self.current_world)
            self.log(f"بکاپ {backup_name}.zip ساخته شد.")
        except Exception as e:
            self.log(f"خطا در بکاپ‌گیری: {e}")

    def manage_world(self):
        worlds = [name for name in os.listdir(SERVER_DIR) if os.path.isdir(os.path.join(SERVER_DIR, name)) and "level.dat" in os.listdir(os.path.join(SERVER_DIR, name))]
        if not worlds:
            QMessageBox.information(self, "وورلدی پیدا نشد", "هیچ وورلدی در پوشه سرور یافت نشد.")
            return
        selected, ok = QInputDialog.getItem(self, "انتخاب وورلد", "یکی از وورلدها را انتخاب کن:", worlds, editable=False)
        if ok and selected:
            self.current_world = os.path.join(SERVER_DIR, selected)
            QMessageBox.information(self, "وورلد فعال شد", f"وورلد فعال به: {selected} تغییر یافت.")

    def install_plugin(self):
        plugin_file, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل پلاگین", "", "All Files (*)")
        if not plugin_file:
            return
        if not os.path.exists(PLUGINS_DIR):
            os.makedirs(PLUGINS_DIR)
        try:
            if plugin_file.endswith(".zip"):
                with zipfile.ZipFile(plugin_file, 'r') as zip_ref:
                    zip_ref.extractall(PLUGINS_DIR)
            else:
                shutil.copy(plugin_file, PLUGINS_DIR)
            self.log(f"پلاگین {os.path.basename(plugin_file)} نصب شد.")
        except Exception as e:
            self.log(f"خطا در نصب پلاگین: {e}")

    def edit_server_properties(self):
        props_path = os.path.join(SERVER_DIR, "server.properties")
        if not os.path.exists(props_path):
            QMessageBox.warning(self, "خطا", "فایل server.properties پیدا نشد!")
            return
        with open(props_path, "r", encoding="utf-8") as f:
            content = f.read()
        text, ok = QInputDialog.getMultiLineText(self, "ویرایش server.properties", "تنظیمات:", content)
        if ok:
            with open(props_path, "w", encoding="utf-8") as f:
                f.write(text)
            self.log("فایل server.properties ذخیره شد.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BedrockServerManager()
    window.show()
    sys.exit(app.exec())

