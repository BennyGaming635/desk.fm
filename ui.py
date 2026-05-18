from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QListWidget, QLabel,
    QFileDialog, QSlider, QListWidgetItem,
    QDialog
)
from PySide6.QtCore import Qt, QSize, QTimer
from utils import extract_cover_image
import os
import vlc
from importwizard import ImportWizard

class MusicUI(QWidget):
    def __init__(self, player):
        super().__init__()
        self.player = player
        
        self.setWindowTitle("DeskFM")
        self.setMinimumSize(900, 600)

        self.cover = QLabel()
        self.cover.setFixedSize(200, 200)
        self.cover.setStyleSheet("background-color: #222; border-radius: 10px;")
        self.cover.setScaledContents(True)

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
        
        self.timer = QTimer ()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.cover)

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

        self.btn_play.setIconSize(QSize(28, 28))
        self.btn_pause.setIconSize(QSize(28, 28))

        self.btn_play.clicked.connect(self.play_selected)
        self.btn_pause.clicked.connect(self.player.pause)

        self.btn_play.setStyleSheet("background-color: transparent;")
        self.btn_pause.setStyleSheet("background-color: transparent;")

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(80)
        self.volume.valueChanged.connect(self.player.set_volume)
        self.progress = QSlider(Qt.Horizontal)
        self.progress.setRange(0, 1000)
        self.progress.sliderMoved.connect(self.seek_position)

        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_pause)
        controls.addStretch()
        controls.addWidget(QLabel("Volume"))
        controls.addWidget(self.volume)
        controls.addWidget(self.progress)

        main_layout.addLayout(controls)

        root.addLayout(self.sidebar, 1)
        root.addLayout(main_layout, 3)

        self.setLayout(root)

        self.setStyleSheet(self.dark_theme())

    def seek_position(self, value):
        if self.player.player:
            duration = self.player.player.get_length()
            if duration > 0:
                self.player.player.set_time(int((value / 1000) * duration))

    def update_progress(self):
        try:
            if not self.player.player:
                return

            duration = self.player.player.get_length()
            current = self.player.player.get_time()

            if duration > 0 and current >= 0:
                value = int((current / duration) * 1000)
                self.progress.blockSignals(True)
                self.progress.setValue(value)
                self.progress.blockSignals(False)

            state = self.player.player.get_state()
            if state == self.player.vlc.State.Ended:
                self.next_song()
        except Exception as e:
            print(e)

    def load_songs(self):
        wizard = ImportWizard(self)

        if wizard.exec() != QDialog.Accepted:
            return
        
        files = wizard.selected_files

        for f in files:
            cover = extract_cover_image(f)

            self.songs.append({
                "path": f,
                "name": os.path.splitext(os.path.basename(f))[0],
                "cover": cover
            })

            self.list_widget.addItem(self.songs[-1]["name"])

    def play_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        
        index = self.list_widget.currentRow()
        song = self.songs[index]

        self.player.load(song["path"])
        QTimer.singleShot(100, self.player.play)

        self.now_playing.setText(f"Now Playing: {song['name']}")
        self.progress.setValue(0)

        if song["cover"]:
            pixmap = QPixmap(song["cover"])
            self.cover.setPixmap(pixmap)
        else:
            self.cover.setPixmap(QPixmap())

    def next_song(self):
        current = self.list_widget.currentRow()
        next_index = current + 1

        if next_index < len(self.songs):
            self.list_widget.setCurrentRow(next_index)
            self.progress.setValue(0)
            self.play_selected()

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
                border-radius: 4px;
            }

            QListWidget {
                background-color: #181818;
                border: none;
                padding: none;
            }

            QListWidget::item {
                padding: 4px;
                border-radius: 4px;
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