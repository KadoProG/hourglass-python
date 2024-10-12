import math
from app.hourglass.dot import Dot
from app.config import GRID_SIZE
from app.utils.find_index import find_index


class Chamber:
    """砂の挙動を制御するクラス"""

    def __init__(self) -> None:
        self.dots: list[Dot] = []
        self._is_positive_sine = True
        self._is_positive_cosine = True

    def add_dot(self, angle: int) -> None:
        """ドットを追加する"""
        self._is_positive_sine = math.sin((angle * math.pi) / 180) >= 0
        self._is_positive_cosine = math.cos((angle * math.pi) / 180) >= 0

        x = 0 if self._is_positive_sine else GRID_SIZE - 1
        y = 0 if self._is_positive_cosine else GRID_SIZE - 1

        self.dots.append(Dot(x, y))

    def remove_dot(self) -> bool:
        """ドットを削除する"""
        x = GRID_SIZE - 1 if self._is_positive_sine else 0
        y = GRID_SIZE - 1 if self._is_positive_cosine else 0

        index = find_index(self.dots, lambda dot: dot.x == x and dot.y == y)

        if index == -1:
            return False
        else:
            del self.dots[index]
            return True

    def next_frame(self, angle: int) -> None:
        """フレームごとの処理"""
        self._is_positive_sine = math.sin((angle * math.pi) / 180) >= 0
        self._is_positive_cosine = math.cos((angle * math.pi) / 180) >= 0

        for dot in self.dots:
            x = dot.x + (1 if self._is_positive_sine else -1)
            y = dot.y + (1 if self._is_positive_cosine else -1)

            is_right_end = False
            is_bottom_end = False

            is_bottom_right_empty = True
            is_bottom_empty = True
            is_bottom_left_empty = True

            # x軸に対して、はみ出し確認と位置調整
            if self._is_positive_sine and x == GRID_SIZE:
                x -= 1
                is_right_end = True
            elif not self._is_positive_sine and x == -1:
                x += 1
                is_right_end = True

            # y軸に対して、はみ出し確認と位置調整
            if self._is_positive_cosine and y == GRID_SIZE:
                y -= 1
                is_bottom_end = True
            elif (not self._is_positive_cosine) and y == -1:
                y += 1
                is_bottom_end = True

            # x軸とy軸の両方該当する場合、保存しアニメーション処理を終了
            if is_right_end and is_bottom_end:
                dot.x = x
                dot.y = y
                continue

            # 他のボールとの衝突判定
            for b in self.dots:
                if b.x == x and b.y == y:
                    is_bottom_empty = False
                if b.x == x and b.y == (y - 1 if self._is_positive_cosine else y + 1):
                    is_bottom_right_empty = False
                if b.x == (x - 1 if self._is_positive_sine else x + 1) and b.y == y:
                    is_bottom_left_empty = False

            if not is_bottom_empty:
                if is_bottom_right_empty:
                    y = y - 1 if self._is_positive_cosine else y + 1
                elif is_bottom_left_empty:
                    x = x - 1 if self._is_positive_sine else x + 1
                else:
                    y = y - 1 if self._is_positive_cosine else y + 1
                    x = x - 1 if self._is_positive_sine else x + 1

            dot.x = x
            dot.y = y
        print(self.dots)
