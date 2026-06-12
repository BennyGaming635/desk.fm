import os
import sys
import vlc

if getattr(sys, "frozen", False):
    base = sys.MEIPASS
    os.environ["VLC_PLUGIN_PATH"] = os.path.join(base, "plugins")

    instance = vlc.Instance(
        f"--plugin-path={os.path.join(base, 'plugins')}"
    )

else:
    instance = vlc.Instance()

class MusicPlayer:
    def __init__(self):
        self.vlc = vlc
        self.instance = instance
        self.player = self.instance.media_player_new()
        self.media = None

    def load(self, path):
        self.media = self.instance.media_new(path)
        self.player.set_media(self.media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
    
    def set_volume(self, volume):
        self.player.audio_set_volume(volume)