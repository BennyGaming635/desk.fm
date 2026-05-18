import sys
from PySide6.QtWidgets import QApplication
from player import MusicPlayer
from ui import MusicUI
from settings import check_github_update

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    window = MusicUI(player)
    window.show()

    update = check_github_update()
    if update:
        print("Latest version:", update["version"])

    sys.exit(app.exec())