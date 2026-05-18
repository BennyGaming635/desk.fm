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
from settings import SettingsDialog, get_theme
from library import add_song, get_all_songs


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

        self.btn_settings = QPushButton("Settings")
        self.btn_settings.clicked.connect(self.open_settings)

        self.sidebar.addWidget(self.title)
        self.sidebar.addWidget(self.btn_load)
        self.sidebar.addWidget(self.btn_settings)
        self.sidebar.addStretch()

        self.timer = QTimer()
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


        self.current_time = QLabel("00:00")
        self.total_time = QLabel("00:00")
        self.progress = QSlider(Qt.Horizontal)
        self.progress.setRange(0, 1000)
        self.progress.sliderMoved.connect(self.seek_position)

        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_pause)
        controls.addStretch()
        controls.addWidget(self.current_time)
        controls.addWidget(self.progress)
        controls.addWidget(self.total_time)
        controls.addSpacing(20)
        controls.addWidget(QLabel("Volume"))
        controls.addWidget(self.volume)
        main_layout.addLayout(controls)
        root.addLayout(self.sidebar, 1)
        root.addLayout(main_layout, 3)
        self.setLayout(root)
        self.apply_theme()
        self.load_library()

    def load_library(self):
        self.songs = []
        self.list_widget.clear()

        rows = get_all_songs()

        for path, title, artist, album, cover in rows:
            self.songs.append({
                "path": path,
                "name": title,
                "cover": cover
            })

            self.list_widget.addItem(title)

    def seek_position(self, value):
        if self.player.player:
            duration = self.player.player.get_length()
            if duration > 0:
                self.player.player.set_time(int((value / 1000) * duration))

    def format_time(self, ms):
        seconds = int(ms /1000)
        mins = seconds // 60
        secs = seconds % 60

        return f"{mins}:{secs:02}"

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
                self.current_time.setText(self.format_time(current))
                self.total_time.setText(self.format_time(duration))

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
            title = os.path.splitext(os.path.basename(f))[0]

            self.songs.append({
                "path": f,
                "name": title,
                "cover": cover
            })

            self.list_widget.addItem(title)

            add_song(
                f,
                title,
                "Unknown Artist",
                "Unknown Album",
                cover
            )

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
        self.current_time.setText("00:00")

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

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            self.apply_theme()


    def apply_theme(self):
        accent = get_theme()["accent"]

        self.setStyleSheet(f"""
            QWidget {{
                background-color: #121212;
                color: white;
            }}

            QPushButton {{
                background-color: transparent;
                border: none;
            }}

            QPushButton:hover {{
                background-color: #222;
                border-radius: 4px;
            }}

            QSlider::handle:horizontal {{
                background: {accent};
            }}

            QSlider::groove:horizontal {{
                background: #333;
            }}

            QListWidget {{
                background-color: #181818;
                border: none;
            }}

            QListWidget::item:selected {{
                background-color: {accent};
            }}
        """)