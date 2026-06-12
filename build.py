import os
import shutil
import subprocess

APP_NAME = "DeskFM"
ENTRY_FILE = "main.py"
ASSETS_DIR = "assets"

VLC_PATH = r"C:\Program Files\VideoLAN\VLC"


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
        cmd += [
            "--add-data",
            f"{ASSETS_DIR}{os.pathsep}{ASSETS_DIR}"
        ]

    if os.path.exists(VLC_PATH):
        cmd += [
            "--add-binary",
            f"{os.path.join(VLC_PATH, 'libvlc.dll')}{os.pathsep}.",
            "--add-binary",
            f"{os.path.join(VLC_PATH, 'libvlccore.dll')}{os.pathsep}.",
        ]

        plugins = os.path.join(VLC_PATH, "plugins")
        if os.path.exists(plugins):
            cmd += [
                "--add-data",
                f"{plugins}{os.pathsep}plugins"
            ]

    subprocess.run(cmd)


if __name__ == "__main__":
    clean()
    build()