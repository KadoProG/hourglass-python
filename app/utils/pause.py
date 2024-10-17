class Pause:
    def __init__(self, pause: bool = False):
        self.pause = pause

    def __call__(self) -> bool:
        return self.pause

    def set(self, pause: bool):
        self.pause = pause
