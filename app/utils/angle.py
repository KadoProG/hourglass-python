class Angle:
    def __init__(self, angle: int = None, is_fixed: bool = False):
        self.__angle = angle if angle is not None else 0
        self.__auto_rotation = 0
        self.__is_fixed = is_fixed

    def __call__(self) -> int:
        return self.__angle

    def set(self, angle: int):
        if self.__is_fixed:
            return
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
        if self.__is_fixed:
            return
        self.__angle += self.__auto_rotation**2 * (
            -1 if self.__auto_rotation < 0 else 1
        )
