class SoundMock:
    def __init__(self):
        self.played = False

    def play(self):
        self.played = True

    def stop(self):
        self.played = False

    def is_playing(self):
        return self.played
