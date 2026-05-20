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
    
    def get_exe_asset(self, release_data):
        for asset in release_data["assets"]:
            name = asset["name"].lower()

            if name.endswith(".exe"):
                return asset["browser_download_url"]
        return None
    
    def download_update(self, url):
        try:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, "deskfm_update.exe")
            r = requests.get(url, stream=True)

            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return output_path
        
        except Exception as e:
            print(f"Error downloading update: {e}")
            return None
        
    def install_update(self):
        avaliable, release = self.update_avaliable()
        if not avaliable:
            return False, "No update avaliable"
        
        exe_url = self.get_exe_asset(release)

        if not exe_url:
            return False, "No executable asset found in the latest release"
        
        downloaded = self.download_update(exe_url)

        if not downloaded:
            return False, "Failed to download the update"
        
        try:
            subprocess.Popen([downloaded])
            sys.exit()

        except Exception as e:
            return False, str(e)
        
        return True, "Update installed successfully"
        