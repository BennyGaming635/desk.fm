import os
import sys
import requests
import subprocess
import tempfile
from packaging import version

APP_VERSION = "1.0.0"
GITHUB_REPO = "bennygaming635/deskfm"

class Updater:
    def __init__(self):
        self.api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

    def get_latest_release(self):
        try:
            r = requests.get(self.api_url, timeout=10)
            data = r.json()

            return {
                "version": data["tag_name"].lstrip("v"),
                "url": data["html_url"],
                "assets": data.get("assets", [])
            }
        
        except Exception as e:
            print(f"Error fetching latest release: {e}")
            return None
        
    def update_avaliable(self):
        latest = self.get_latest_release()
        if not latest:
            return False, None
        
        latest_version = latest["version"]

        if version.parse(latest_version) > version.parse(APP_VERSION):
            return True, latest
        return False, None