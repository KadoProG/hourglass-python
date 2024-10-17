import math
from app.hourglass.dot import Dot
from app.utils.find_index import find_index


class Chamber:
    """砂の挙動を制御するクラス"""

    def __init__(self, grid_size: int) -> None:
        self.dots: list[Dot] = []
        self._is_positive_sine = True
        self._is_positive_cosine = True
        self._grid_size = grid_size

    def add_dot(self, angle: int) -> None:
        """ドットを追加する"""
        self._is_positive_sine = math.sin((angle * math.pi) / 180) >= 0
        self._is_positive_cosine = math.cos((angle * math.pi) / 180) >= 0

        x = 0 if self._is_positive_sine else self._grid_size - 1
        y = 0 if self._is_positive_cosine else self._grid_size - 1

        self.dots.append(Dot(x, y))

    def remove_dot(self) -> bool:
        """ドットを削除する"""
        x = self._grid_size - 1 if self._is_positive_sine else 0
        y = self._grid_size - 1 if self._is_positive_cosine else 0

        index = find_index(self.dots, lambda dot: dot.x == x and dot.y == y)

        if index == -1:
            return False
        else:
            del self.dots[index]
            return True

    def remove_all(self) -> int:
        """全てのドットを削除する"""
        length = len(self.dots)
        self.dots = []
        return length

    def next_frame(self, angle: int) -> None:
        """フレームごとの処理"""
        self._is_positive_sine = math.sin((angle * math.pi) / 180) >= 0
        self._is_positive_cosine = math.cos((angle * math.pi) / 180) >= 0

        for index, dot in enumerate(self.dots):
            x = dot.x + (1 if self._is_positive_sine else -1)
            y = dot.y + (1 if self._is_positive_cosine else -1)

            is_right_end = False
            is_bottom_end = False

            is_bottom_right_empty = True
            is_bottom_empty = True
            is_bottom_left_empty = True

            # x軸に対して、はみ出し確認と位置調整
            if self._is_positive_sine and x == self._grid_size:
                x -= 1
                is_right_end = True
            elif not self._is_positive_sine and x == -1:
                x += 1
                is_right_end = True

            # y軸に対して、はみ出し確認と位置調整
            if self._is_positive_cosine and y == self._grid_size:
                y -= 1
                is_bottom_end = True
            elif (not self._is_positive_cosine) and y == -1:
                y += 1
                is_bottom_end = True

            # x軸とy軸のともに奥の状態の場合、保存しアニメーション処理を終了
            if is_right_end and is_bottom_end:
                dot.x = x
                dot.y = y
                continue

            # 他のボールとの衝突判定
            for index2, b in enumerate(self.dots):
                if index == index2:
                    continue
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
