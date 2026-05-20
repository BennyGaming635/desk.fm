from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen import File
import os

def extract_cover_image(path):
    try:
        audio = MP3(path, ID3=ID3)

        if not audio.tags:
            return None

        for tag in audio.tags.values():
            if isinstance(tag, APIC):

                cover_path = path + "_cover.jpg"

                with open(cover_path, "wb") as img:
                    img.write(tag.data)

                return cover_path

    except Exception as e:
        print("Cover error:", e)

    return None

    
def get_song_metadata(path):
    audio = File(path)

    title = None
    artist = "Unknown Artist"
    album = "Unknown Album"

    try:
        if audio is not None and audio.tags:

            if "TIT2" in audio:
                title = str(audio["TIT2"])

            if "TPE1" in audio:
                artist = str(audio["TPE1"])

            if "TALB" in audio:
                album = str(audio["TALB"])

            if not title and hasattr(audio, "tags"):
                tags = audio.tags
                if tags:
                    for key in ["title", "TIT2"]:
                        if key in tags:
                            title = str(tags[key][0])

    except Exception:
        pass

    if not title:
        title = os.path.splitext(os.path.basename(path))[0]

    return {
        "title": title,
        "artist": artist,
        "album": album
    }