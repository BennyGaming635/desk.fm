import json
import os
import requests
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox
)
from updater import Updater

CONFIG_FILE = "config.json"

THEMES = {
    "Classic Green": {
        "accent": "#1DB954",
    },
    "Blueberry Blue": {
        "accent": "#343deb",
    },
    "Bombastic Orange": {
        "accent": "#F97316"
    }
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"theme": "Classic Green"}

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    
def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_theme():
    config = load_config()
    return THEMES.get(config.get("theme", "Classic Green"), THEMES["Classic Green"])

def check_github_update():
    try:
        url = "https://api.github.com/repos/bennygaming635/deskfm/releases/latest"
        r = requests.get(url, timeout=5)
        data = r.json()

        return {
            "version": data["tag_name"],
            "url": data["html_url"]
        }
    except:
        return None
    
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setMinimumSize(350, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Theme")
        self.combo = QComboBox()
        self.view_label = QLabel("View")
        
        self.view_combo = QComboBox()
        self.view_combo.addItems(["List View", "Tile View"])

        for theme in THEMES.keys():
            self.combo.addItem(theme)

        config = load_config()
        self.combo.setCurrentText(config.get("theme", "Classic Green"))
        self.view_combo.setCurrentText(config.get("view_mode", "List View"))

        self.save_btn = QPushButton("Save")
        self.install_btn = QPushButton("Install Updates")

        self.save_btn.clicked.connect(self.save)
        self.install_btn.clicked.connect(self.install_update)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.view_label)
        layout.addWidget(self.view_combo)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.install_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: white;
            }

            QPushButton {
                background-color: #1DB954;
                border: none;
                padding: 8px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #1ed760;
            }
        """)

    def save(self):
        save_config({
            "theme": self.combo.currentText(),
            "view_mode": self.view_combo.currentText()
        })
        self.accept()

    def check_update(self):
        updater = Updater()
        avaliable, release = updater.update_avaliable()

        if avaliable:
            self.label.setText(
                f"Update Available: {release['version']}"
            )
        else:
            self.label.setText("No updates available")

    def install_update(self):
        updater = Updater()
        success, message = updater.install_update()

        if success:
            self.label.setText("Update installed successfully")
        else:
            self.label.setText(f"Update failed: {message}")


def get_view_mode():
    config = load_config()
    return config.get("view_mode", "List View")