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

    c.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS playlist_songs (
            playlist_id INTEGER,
            song_path TEXT
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

def create_playlist(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO playlists(name) VALUES(?)",
        (name,)
    )
    conn.commit()
    conn.close()

def get_playlists():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name FROM playlists")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def add_song_to_playlist(playlist_id, song_path):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute(
        "SELECT id FROM playlists WHERE name=?",
        (playlist_id,)
    )
    result = c.fetchone()

    if not result:
        conn.close()
        return
    
    playlist_id = result[0]

    c.execute(
        """
        INSERT INTO playlist_songs
        (playlist_id, song_path)
        VALUES (?, ?)
        """,
        (playlist_id, song_path)
    )

    conn.commit()
    conn.close()

def get_playlist_songs(playlist):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    SELECT song.path, songs.title, songs.artist,
              songs.album, songs.cover
    FROM songs
    JOIN playlist_songs
    ON songs.path = playlist_songs.song_path
    JOIN playlists
    ON playlists.id = playlist_spngs.playlist_id
    WHERE playlists.name = ?
    """, (playlist,))

    rows = c.fetchall()
    conn.close()
    return rows


