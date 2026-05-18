import vlc

class MusicPlayer:
    def __init__(self):
        self.vlc = vlc
        self.instance = vlc.Instance()
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