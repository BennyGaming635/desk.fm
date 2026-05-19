import sys
from PySide6.QtWidgets import QApplication
from player import MusicPlayer
from ui import MusicUI
from PySide6.QtGui import QIcon
from settings import check_github_update
from library import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icon.png"))
    player = MusicPlayer()
    window = MusicUI(player)
    window.show()

    update = check_github_update()
    if update:
        print("Latest version:", update["version"])

    sys.exit(app.exec())