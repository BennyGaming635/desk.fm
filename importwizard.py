import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QFileDialog
)


class ImportWizard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Import Wizard")
        self.setMinimumSize(400, 250)

        self.selected_files = []

        layout = QVBoxLayout()

        title = QLabel("Import Music")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        desc = QLabel(
            "Choose how you want to import your music library into DeskFM."
        )
        desc.setWordWrap(True)

        self.btn_folder = QPushButton("Import Music Folder")
        self.btn_files = QPushButton("Import Individual Songs")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_folder.clicked.connect(self.import_folder)
        self.btn_files.clicked.connect(self.import_files)
        self.btn_cancel.clicked.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(20)
        layout.addWidget(self.btn_folder)
        layout.addWidget(self.btn_files)
        layout.addStretch()
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: white;
            }

            QPushButton {
                background-color: #1DB954;
                border: none;
                padding: 10px;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #1ed760;
            }
        """)

    def import_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")

        if not folder:
            return

        supported = (".mp3", ".wav", ".ogg")

        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(supported):
                    self.selected_files.append(os.path.join(root, file))

        self.accept()

    def import_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Music",
            "",
            "Audio Files (*.mp3 *.wav *.ogg)"
        )

        if files:
            self.selected_files = files
            self.accept()