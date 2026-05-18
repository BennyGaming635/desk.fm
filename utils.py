from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
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