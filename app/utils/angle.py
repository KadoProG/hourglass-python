class Angle:
    def __init__(self, angle: int = None):
        self.__angle = angle if angle is not None else 0
        self.__auto_rotation = 0

    def __call__(self) -> int:
        return self.__angle

    def set(self, angle: int):
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360
        self.__angle = angle

    def get_auto_rotation(self) -> int:
        return self.__auto_rotation

    def set_auto_rotation(self, auto_rotation: int):
        self.__auto_rotation += auto_rotation

    def next_frame(self):
        self.__angle += self.__auto_rotation**2 * (
            -1 if self.__auto_rotation < 0 else 1
        )
