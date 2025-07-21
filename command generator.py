from __future__ import print_function
import sys, datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QCompleter, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor, QFont, QTextCursor
from PyQt5.QtCore import Qt

from mctools import RCONClient             # فقط 3.6+ نیاز دارد
from colorama import init as colorama_init # برای حالت CLI (اختیاری)

# ---------- تنظیم رنگِ تاریک سراسری ----------
def enable_dark(app):
    app.setStyle("Fusion")
    pal = QPalette()
    base   = QColor(45, 45, 45)
    back   = QColor(36, 36, 36)
    text   = QColor(220, 220, 220)
    accent = QColor(85, 170, 255)

    pal.setColor(QPalette.Window, back)
    pal.setColor(QPalette.WindowText, text)
    pal.setColor(QPalette.Base, base)
    pal.setColor(QPalette.AlternateBase, back)
    pal.setColor(QPalette.ToolTipBase, text)
    pal.setColor(QPalette.ToolTipText, text)
    pal.setColor(QPalette.Text, text)
    pal.setColor(QPalette.Button, base)
    pal.setColor(QPalette.ButtonText, text)
    pal.setColor(QPalette.BrightText, accent)
    pal.setColor(QPalette.Link, accent)
    pal.setColor(QPalette.Highlight, accent.darker())
    pal.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(pal)

# ---------- لیست خلاصه‌ای از دستورات Bedrock برای auto-complete ----------
COMMANDS = [
    "/say", "/tell", "/tp", "/give", "/effect", "/summon", "/execute",
    "/fill", "/setblock", "/tag", "/testfor", "/title", "/particle",
    "/kill", "/clear", "/gamemode", "/difficulty", "/locate", "/function",
    "/scoreboard", "/time", "/weather", "/spawnpoint", "/setworldspawn",
    # می‌توانی هر دستوری را که خواستی اضافه کنی…
]

# ---------- Wrapper ساده برای mctools.RCONClient ----------
class _RCON(object):
    def __init__(self):
        self.client = None
        self.connected = False

    def connect(self, host, port, password):
        self.client = RCONClient(host, port=int(port))
        if not self.client.login(password):
            raise RuntimeError("ورود RCON رد شد (پسورد/پورت درست نیست)")
        self.connected = True

    def disconnect(self):
        if self.client:
            try:
                self.client.disconnect()
            finally:
                self.connected = False
                self.client = None

    def command(self, cmd):
        if not self.connected:
            raise RuntimeError("در حالت آفلاین هستی")
        return self.client.command(cmd.lstrip("/"))  # mctools نیازی به اسلش اول ندارد

# ---------- پنجرهٔ اصلی ----------
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Bedrock Command Studio")
        self.resize(840, 620)

        # مرکز
        cw = QWidget(self)
        self.setCentralWidget(cw)
        v = QVBoxLayout(cw)

        # نوار اتصال
        top = QHBoxLayout()
        self.host   = QLineEdit(); self.host.setPlaceholderText("Host")
        self.port   = QLineEdit("19132"); self.port.setFixedWidth(70)
        self.passwd = QLineEdit(); self.passwd.setPlaceholderText("Password"); self.passwd.setEchoMode(QLineEdit.Password)
        self.btn    = QPushButton("Connect")
        self.btn.clicked.connect(self.toggle_connection)
        for w in (QLabel("RCON:"), self.host, self.port, self.passwd, self.btn):
            top.addWidget(w)
        v.addLayout(top)

        # فیلد دستور
        self.inp = QLineEdit(); self.inp.setPlaceholderText("مثال: /say Hello World ❤")
        self.inp.setFont(QFont("Consolas", 10))
        self.inp.returnPressed.connect(self.run_cmd)
        self.inp.setCompleter(QCompleter(COMMANDS))
        v.addWidget(self.inp)

        # لاگ
        self.log = QTextEdit(); self.log.setReadOnly(True); self.log.setFont(QFont("Consolas", 10))
        v.addWidget(self.log, 1)

        # RCON core
        self.rcon = _RCON()

    # ---------- اتصال / قطع ----------
    def toggle_connection(self):
        if self.rcon.connected:
            self.rcon.disconnect()
            self.btn.setText("Connect")
            self._println("◇ Disconnected", "yellow")
            return

        host, port, pwd = self.host.text().strip(), self.port.text().strip(), self.passwd.text()
        if not (host and pwd):
            QMessageBox.warning(self, "Bedrock Command Studio", "Host و Password را پر کن یا در حالت آفلاین بمان.")
            return
        try:
            self.rcon.connect(host, port, pwd)
            self.btn.setText("Disconnect")
            self._println("✓ RCON connected", "green")
        except Exception as e:
            QMessageBox.critical(self, "Bedrock Command Studio", str(e))
            self._println("⛔ "+str(e), "red")

    # ---------- اجرای دستور ----------
    def run_cmd(self):
        raw = self.inp.text().strip()
        if not raw:
            return
        self._println("> "+raw, "cyan")

        # چک سطحی سینتکس: با / شروع شود
        if not raw.startswith("/"):
            self._println("⛔ باید با / شروع شود", "red")
            return
        self._println("✓ Looks fine (basic check)", "green")

        if self.rcon.connected:
            try:
                resp = self.rcon.command(raw)
                self._println(resp or "(no response)", "magenta")
            except Exception as e:
                self._println("⛔ "+str(e), "red")
        else:
            self._println("◇ Offline mode (هیچ چیز به سرور نفرستاده شد)", "yellow")
        self.inp.clear()

    # ---------- لاگ رنگی ----------
    def _println(self, txt, color="white"):
        cursor = self.log.textCursor()
        self.log.setTextColor(QColor(color))
        self.log.append(u"[{}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), txt))
        self.log.moveCursor(QTextCursor.End)

# ---------- اجرا ----------
def main():
    colorama_init()

    app = QApplication(sys.argv)
    enable_dark(app)
    win = Main(); win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
