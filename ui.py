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
        
        set.setWindowTitle("DeskFM")
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

        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_stop = QPushButton("Stop")

        self.btn_play.clicked.connect(self.play_selected)
        self.btn_pause.clicked.connect(self.player.pause)
        self.btn_stop.clicked.connect(self.player.stop)

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(80)
        self.volume.valueChanged.connect(self.player.set_volume)

        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_pause)
        controls.addWidget(self.btn_stop)
        controls.addStretch()
        controls.addWidget(QLabel("Volume"))
        controls.addWidget(self.volume)

        main_layout.addLayout(controls)

        root.addLayout(self.sidebar, 1)
        root.addLayout(main_layout, 3)

        self.setLayout(root)

        self.setStyleSheet(self.dark_theme())