import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon, QMenu
from player import MusicPlayer
from ui import MusicUI
from PySide6.QtGui import QIcon, QAction
from settings import check_github_update
from library import init_db
import vlc
    
def check_vlc():
    try:
        vlc.Instance()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icon.png"))
    if not check_vlc():
        QMessageBox.critical(
            None,
            "VLC Required",
            "DeskFM requires VLC Media Player to be installed."
        )
        sys.exit(1)

    player = MusicPlayer()
    window = MusicUI(player)
    window.show()

    tray = QSystemTrayIcon()
    tray.setIcon(QIcon("assets/icon.png"))
    tray.setVisible(True)
    tray_menu = QMenu()
    show_action = QAction("Show")
    quit_action = QAction("Quit")
    show_action.triggered.connect(window.show)
    quit_action.triggered.connect(app.quit)
    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)
    tray.setContextMenu(tray_menu)

    update = check_github_update()
    if update:
        print("Latest version:", update["version"])

    sys.exit(app.exec())