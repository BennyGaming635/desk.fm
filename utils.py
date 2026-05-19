from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen import File
import os

def extract_cover_image(audio_path):
    audio = File(audio_path)

    if not audio:
        return None
    
    try:
        if "APIC:" in audio.tags:
            art = audio.tags["APIC:"].data
        else:
            return None
        
        cover_path = audio_path + "_cover.jpg"
        with open(cover_path, "wb") as f:
            f.write(art)
        
        return cover_path
    except Exception:
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