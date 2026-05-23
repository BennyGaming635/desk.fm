import os
import shutil
import subprocess

APP_NAME = "DeskFM"
ENTRY_FILE = "main.py"
ASSETS_DIR = "assets"


def clean():
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)


def build():
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",
        "--name", APP_NAME,
        ENTRY_FILE,
    ]

    if os.path.exists(ASSETS_DIR):
        cmd += ["--add-data", f"{ASSETS_DIR}{os.pathsep}{ASSETS_DIR}"]

    subprocess.run(cmd)


if __name__ == "__main__":
    clean()
    build()