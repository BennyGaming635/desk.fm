from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QListWidget, QLabel,
    QFileDialog, QSlider, QListWidgetItem
)
from PySide6.QtCore import Qt

class MusicUI(QWidget):
    def __init__(self, player):
        super().__init__()
        self.player = player
        
        self.setWindowTitle("DeskFM")
        self.setMinimumSize(900, 600)

        self.songs = []

        root = QHBoxLayout()

        self.sidebar = QVBoxLayout()

        self.title = QLabel("DeskFM")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        
        self.btn_load = QPushButton("Import Music")
        self.btn_load.clicked.connect(self.load_songs)

        self.sidebar.addWidget(self.title)
        self.sidebar.addWidget(self.btn_load)
        self.sidebar.addStretch()

        main_layout = QVBoxLayout()

        self.now_playing = QLabel("Nothing is playing")
        self.now_playing.setStyleSheet("font-size: 18px;")

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.play_selected)

        main_layout.addWidget(self.now_playing)
        main_layout.addWidget(self.list_widget)

        controls = QHBoxLayout()

        self.btn_play = QPushButton()
        self.btn_pause = QPushButton()

        self.btn_pause.setIcon(QIcon("assets/icons/pause.svg"))
        self.btn_play.setIcon(QIcon("assets/icons/play.svg"))

        self.btn_play.setIconSize(Qt.QSize(28, 28))
        self.btn_pause.setIconSize(Qt.QSize(28, 28))

        self.btn_play.clicked.connect(self.play_selected)
        self.btn_pause.clicked.connect(self.player.pause)

        self.btn_play.setStyleSheet("background-color: transparent;")
        self.btn_pause.setStyleSheet("background-color: transparent;")

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(80)
        self.volume.valueChanged.connect(self.player.set_volume)

        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_pause)
        controls.addStretch()
        controls.addWidget(QLabel("Volume"))
        controls.addWidget(self.volume)

        main_layout.addLayout(controls)

        root.addLayout(self.sidebar, 1)
        root.addLayout(main_layout, 3)

        self.setLayout(root)

        self.setStyleSheet(self.dark_theme())

    def load_songs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Music Files", "", "Audio Files (*.mp3 *.wav *.ogg)")
        for f in files:
            self.songs.append(f)
            item = QListWidgetItem(f.split("/")[-1])
            self.list_widget.addItem(item)

    def play_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        
        index = self.list_widget.currentRow()
        song = self.songs[index]

        self.player.load(song)
        self.player.play()

        self.now_playing.setText(f"Now Playing: {item.text()}")

    def dark_theme(self):
        return """
            QWidget {
                background-color: #121212;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
            }
            
            QPushButton {
                background-color: transparent;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #222;
                border-radius: 8px;
            }

            QListWidget {
                background-color: #181818;
                border: none;
                padding: none;
            }

            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
            }

            QListWidget::item:selected {
                background-color: #333333;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background: #333;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                width: 12px;
                background: #1DB954;
                border-radius: 6px;
            }
            """