import sys
from PySide6.QtWidgets import QApplication
from player import MusicPlayer
from ui import MusicUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    window = MusicUI(player)
    window.show()

    sys.exit(app.exec())