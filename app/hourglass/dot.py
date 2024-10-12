class Dot:
    """砂の粒子を表すクラス"""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y
