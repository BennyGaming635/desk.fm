import sqlite3
import os

DB_FILE = "music.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            title TEXT,
            artist TEXT,
            album TEXT,
            cover TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_song(path, title, artist, album, cover):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO songs (path, title, artist, album, cover)
        VALUES (?, ?, ?, ?, ?)
    """, (path, title, artist, album, cover))

    conn.commit()
    conn.close()


def get_all_songs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT path, title, artist, album, cover FROM songs")
    rows = c.fetchall()

    conn.close()
    return rows

def remove_song(path):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute(
        "DELETE FROM songs WHERE path = ?", (path,)
    )

    conn.commit()
    conn.close()