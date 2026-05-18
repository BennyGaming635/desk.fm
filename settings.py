import json
import os
import requests
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox
)

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

        for theme in THEMES.keys():
            self.combo.addItem(theme)

        config = load_config()
        self.combo.setCurrentText(config.get("theme", "Classic Green"))

        self.save_btn = QPushButton("Save")
        self.update_btn = QPushButton("Check for Updates")

        self.save_btn.clicked.connect(self.save)
        self.update_btn.clicked.connect(self.check_update)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.update_btn)

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
        save_config({"theme": self.combo.currentText()})
        self.accept()

    def check_update(self):
        update = check_github_update()

        if update:
            self.label.setText(f"Latest Version: {update['version']}")
        else:
            self.label.setText("Could not check for updates")