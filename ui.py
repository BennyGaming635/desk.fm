from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QLabel, QSlider
)
from PySide6.QtCore import Qt

class MusicUI(QWidget):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setWindowTitle("DeskFM")
        self.layout = QVBoxLayout()
        self.setMinimumSize(500, 400)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.label = QLabel("No song loaded")
        self.layout.addWidget(self.label)
        
        self.btn_load = QPushButton("Load Song")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_stop = QPushButton("Stop")

        self.layout.addWidget(self.btn_load)
        self.layout.addWidget(self.btn_play)
        self.layout.addWidget(self.btn_pause)
        self.layout.addWidget(self.btn_stop)

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(80)
        self.layout.addWidget(self.volume)

        self.setLayout(self.layout)

        self.songs = []

        self.btn_load.clicked.connect(self.load_songs)
        self.btn_play.clicked.connect(self.play_song)
        self.btn_pause.clicked.connect(self.player.pause)
        self.btn_stop.clicked.connect(self.player.stop)
        self.volume.valueChanged.connect(self.player.set_volume)

    def load_songs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Songs", "", "Audio Files (*.mp3 *.wav *.ogg)"
        )

        for f in files:
            self.songs.append(f)
            self.list_widget.addItem(f.split("/")[-1])

    def play_song(self):
        index = self.list_widget.currentRow()
        if index >= 0:
            song = self.songs[index]
            self.player.load(song)
            self.player.play()
            self.label.setText(f"Playing: {song.split('/')[-1]}")