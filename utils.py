from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen import File
import os

def extract_cover_image(audio_path):
    try:
        audio = MP3(audio_path, ID3=ID3)
        tags = audio.tags

        if not tags:
            return None
        
        for tag in tags.values():
            if isinstance(tag, APIC):
                cover_path = audio_path + "_cover.jpg"

                with open(cover_path, "wb") as img:
                    img.write(tag.data)

                return cover_path
            
    except Exception as e:
        print(f"Error extracting cover from {audio_path}: {e}")
        return None
    
    def get_song_metadata(path):
        audio = File(path)
        title = None
        artist = "Unknown Artist"
        album = "Unknown Album"

        try:
            if audio.tags:
                if "TIT2" in audio.tags:
                    title = str(audio.tags["TIT2"])
                
                if "TPE1" in audio.tags:
                    artist = str(audio.tags["TPE1"])

                if "TALB" in audio.tags:
                    album = str(audio.tags["TALB"])

                if not title and "title" in audio:
                    title = audio["title"][0]

                if "artist" in audio:
                    artist = audio["artist"][0]

                if "album" in audio:
                    album = audio["album"][0]

        except Exception as e:
            print(f"Error extracting metadata from {path}: {e}")

        if not title:
            title = os.path.splitext(
                os.path.basename(path)
            )[0]

        return {
            "title": title,
            "artist": artist,
            "album": album
        }