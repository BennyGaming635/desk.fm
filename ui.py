from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QListWidget, QLabel,
    QFileDialog, QSlider, QListWidgetItem,
    QDialog, QSizePolicy, QLineEdit,
    QMenu, QInputDialog
)
from PySide6.QtCore import Qt, QSize, QTimer
from utils import extract_cover_image, get_song_metadata
import os
import vlc
from importwizard import ImportWizard
from settings import (
    SettingsDialog, get_theme, get_view_mode
)
from library import (
    add_song,
    get_all_songs,
    remove_song,
    create_playlist,
    get_playlists,
    add_song_to_playlist,
    get_playlist_songs,
    delete_playlist
)

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

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search songs...")
        self.search_bar.textChanged.connect(self.search_library)

        self.songs = []
        self.queue = []

        root = QHBoxLayout()
        self.sidebar = QVBoxLayout()

        self.sidebar.addStretch()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.cover)
        self.queue_panel = QListWidget()
        self.queue_panel.setMinimumWidth(200)
        self.queue_panel.setVisible(False)
        root.addLayout(self.sidebar, 3.5)
        root.addLayout(main_layout, 77.5)
        root.addWidget(self.queue_panel, 20)

        self.now_playing = QLabel("Nothing is playing")
        self.now_playing.setStyleSheet("font-size: 18px;")

        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(48, 48))
        self.list_widget.itemClicked.connect(self.play_selected)
        self.apply_view_mode()

        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        main_layout.addWidget(self.now_playing)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.search_bar)

        controls = QHBoxLayout()

        self.btn_play = QPushButton()
        self.btn_pause = QPushButton()

        self.btn_pause.setIcon(QIcon("assets/icons/pause.svg"))
        self.btn_play.setIcon(QIcon("assets/icons/play.svg"))

        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(QIcon("assets/icons/settings.svg"))
        self.btn_settings.setIconSize(QSize(28, 28))
        self.btn_settings.setFixedSize(30, 30)
        self.btn_settings.clicked.connect(self.open_settings)
        self.sidebar.addWidget(self.btn_settings, alignment=Qt.AlignLeft)
        self.btn_load = QPushButton()
        self.btn_load.setIcon(QIcon("assets/icons/import.svg"))
        self.btn_load.setIconSize(QSize(28, 28))
        self.btn_load.setFixedSize(30, 30)
        self.btn_load.clicked.connect(self.load_songs)
        self.sidebar.addWidget(self.btn_load, alignment=Qt.AlignLeft)
        self.btn_queue = QPushButton()
        self.btn_queue.setIcon(QIcon("assets/icons/queue.svg"))
        self.btn_queue.setIconSize(QSize(28, 28))
        self.btn_queue.setFixedSize(30, 30)
        self.btn_queue.clicked.connect(self.toggle_queue)
        self.sidebar.addWidget(self.btn_queue, alignment=Qt.AlignLeft)
        self.btn_new_playlist = QPushButton()
        self.btn_new_playlist.setIcon(QIcon("assets/icons/playlist.svg"))
        self.btn_new_playlist.setIconSize(QSize(28, 28))
        self.btn_new_playlist.setFixedSize(30, 30)
        self.btn_new_playlist.clicked.connect(self.create_playlist_ui)
        self.sidebar.addWidget(self.btn_new_playlist, alignment=Qt.AlignLeft)
        self.btn_library = QPushButton()
        self.btn_library.setIcon(QIcon("assets/icons/library.svg"))
        self.btn_library.setIconSize(QSize(28, 28))
        self.btn_library.setFixedSize(30, 30)
        self.btn_library.clicked.connect(self.home)
        self.sidebar.addWidget(self.btn_library, alignment=Qt.AlignLeft)

        self.playlist_label = QLabel("Playlists")
        self.sidebar.addWidget(self.playlist_label, alignment=Qt.AlignLeft)
        self.playlists = QListWidget()
        self.playlists.itemClicked.connect(self.open_playlist)
        self.sidebar.addWidget(self.playlists)
        self.playlists.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlists.customContextMenuRequested.connect(self.show_playlist_menu)

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
        self.setLayout(root)
        self.apply_theme()
        self.load_library()
        self.load_playlists()

    def home(self):
        self.search_library("")

    def load_library(self):
        self.search_bar.clear()
        self.songs = []
        self.list_widget.clear()

        rows = get_all_songs()

        for path, title, artist, album, cover in rows:
            self.songs.append({
                "path": path,
                "name": title,
                "artist": artist,
                "album": album,
                "cover": cover
            })

            item = QListWidgetItem(title)

            if cover and os.path.exists(cover):
                item.setIcon(QIcon(cover))

        self.list_widget.addItem(item)

    def remove_from_library(self, index):
        song = self.songs[index]
        remove_song(song["path"])
        self.songs.pop(index)
        self.list_widget.takeItem(index)

    def show_context_menu(self, pos):
        item = self.list_widget.itemAt(pos)
        if not item:
            return
        
        menu = QMenu()

        add_queue = menu.addAction("Add to Queue")
        remove_library = menu.addAction("Remove from Library")
        add_playlist = menu.addAction("Add to Playlist")

        action = menu.exec(self.list_widget.viewport().mapToGlobal(pos)
        )

        index = self.list_widget.row(item)
        song = self.songs[index]

        if action == add_queue:
            index = self.list_widget.row(item)
            song = self.songs[index]
            self.add_to_queue(song)

        elif action == remove_library:
            self.remove_from_library(index)

        elif action == add_playlist:
            playlists = get_playlists()

            playlist, ok = QInputDialog.getItem(
                self,
                "Add to Playlist",
                "Playlist:",
                playlists,
                0,
                False
            )

            if ok and playlist:
                add_song_to_playlist(
                    playlist,
                    song["path"]
                )
    
    def show_playlist_menu(self, pos):
        item = self.playlists.itemAt(pos)

        if not item:
            return
        
        menu = QMenu()

        delete_action = menu.addAction("Delete Playlist")
        queue_action = menu.addAction("Queue Playlist")
        action = menu.exec(self.playlists.viewport().mapToGlobal(pos))

        if action == delete_action:
            delete_playlist(item.text())
            self.load_playlists()
            self.home()

        elif action == queue_action:
            songs = get_playlist_songs(item.text())
            for path, title, artist, album, cover in songs:
                self.add_to_queue({
                    "path": path,
                    "name": title,
                    "artist": artist,
                    "album": album,
                    "cover": cover
                })

    def search_library(self, text):
        self.list_widget.clear()
        rows = get_all_songs()
        text = text.lower().strip()
        self.songs = []
        for path, title, artist, album, cover in rows:
            haystack = f"{title} {artist} {album}".lower()
            if text in haystack:
                self.songs.append({
                    "path": path,
                    "name": title,
                    "artist": artist,
                    "album": album,
                    "cover": cover
                })
                item = QListWidgetItem(title)
                if cover and os.path.exists(cover):
                    item.setIcon(QIcon(cover))
                self.list_widget.addItem(item)

    def toggle_queue(self):
        self.queue_panel.setVisible(not self.queue_panel.isVisible())

    def add_to_queue(self, song):
        self.queue.append(song)
        self.queue_panel.addItem(song["name"])

    def set_tile_view(self):
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(120, 120))
        self.list_widget.setGridSize(QSize(140, 160))

    def set_list_view(self):
        self.list_widget.setViewMode(QListWidget.ListMode)
        self.list_widget.setIconSize(QSize(48, 48))
        self.list_widget.setGridSize(QSize())

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
    
    def load_playlists(self):
        self.playlists.clear()

        for playlist in get_playlists():
            self.playlists.addItem(playlist)

    def create_playlist_ui(self):
        name, ok = QInputDialog.getText(self, "New Playlist", "Enter playlist name:")

        if ok and name:
            create_playlist(name)
            self.load_playlists()

    def open_playlist(self, item):
        playlist = item.text()

        self.songs = []
        self.list_widget.clear()

        rows = get_playlist_songs(playlist)

        for path, title, artist, album, cover in rows:
            self.songs.append({
                "path": path,
                "name": title,
                "cover": cover
            })

            song_item = QListWidgetItem(title)
            if cover:
                song_item.setIcon(QIcon(cover))

            self.list_widget.addItem(song_item)

    def apply_view_mode(self):
        mode = get_view_mode()

        if mode == "Tile View":
            self.set_tile_view()
        else:
            self.set_list_view()

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
            metadata = get_song_metadata(f)
            title = metadata["title"]
            artist = metadata["artist"]
            album = metadata["album"]

            self.songs.append({
                "path": f,
                "name": title,
                "cover": cover
            })

            item = QListWidgetItem(title)
            if cover and os.path.exists(cover):
                item.setIcon(QIcon(cover))
            self.list_widget.addItem(item)

            add_song(
                f,
                title,
                artist,
                album,
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

        if song["cover"] and os.path.exists(song["cover"]):
            pixmap = QPixmap(song["cover"])
            self.cover.setPixmap(pixmap)
        else:
            self.cover.setPixmap(QPixmap())

    def next_song(self):
        if self.queue:
            song = self.queue.pop(0)
            self.queue_panel.takeItem(0)

            self.player.load(song["path"])
            QTimer.singleShot(100, self.player.play)

            self.now_playing.setText(f"Now Playing: {song['name']}")
            self.progress.setValue(0)
            self.current_time.setText("00:00")

            if song["cover"] and os.path.exists(song["cover"]):
                pixmap = QPixmap(song["cover"])
                self.cover.setPixmap(pixmap)
            else:
                self.cover.setPixmap(QPixmap())

            return
        
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
            self.apply_view_mode()


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