from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class FullScreenPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Now Playing")
        self.hide()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        
        self.cover = QLabel()
        self.cover.setFixedSize(500, 500)
        self.cover.setScaledContents(True)
        self.cover.setStyleSheet("border-radius: 20px;")

        self.song_title = QLabel("Nothing Playing")
        self.song_title.setAlignment(Qt.AlignCenter)
        self.song_title.setStyleSheet("font-size: 36px; font-weight: bold; color: white;")

        self.layout.addWidget(self.cover)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.song_title)

        self.setLayout(self.layout)
        
        self.setStyleSheet("QWidget { background-color: #121212; }")

    def update_song(self, title, cover_path):
        self.song_title.setText(title)

        if cover_path:
            pixmap = QPixmap(cover_path)
            self.cover.setPixmap(pixmap)
        else:
            self.cover.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()