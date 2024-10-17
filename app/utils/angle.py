class Angle:
    def __init__(self, angle: int = None):

        self.__angle = angle if angle is not None else 0

    def __call__(self) -> int:
        return self.__angle

    def set(self, angle: int) -> int:
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360
        self.__angle = angle
        return self.__angle
