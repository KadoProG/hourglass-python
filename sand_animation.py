import math
from config import GRID_SIZE, INIT_ANGLE
from typing import Optional


class SandAnimation:
    _balls = [[], []]
    _angle = INIT_ANGLE
    _is_positive_sine = True
    _is_positive_cosine = True
    _is_finish_falling = False

    def __init__(self, draw, sound) -> None:
        self.draw = draw
        self._sound = sound

    def next_frame(self) -> tuple[list[list[dict[str, int]]], int, bool]:
        """次のフレームを計算する"""
        self._is_positive_sine = math.sin((self._angle * math.pi) / 180) >= 0
        self._is_positive_cosine = math.cos((self._angle * math.pi) / 180) >= 0
        for canvas_index in range(len(self._balls)):
            for index, ball in enumerate(self._balls[canvas_index]):
                x = ball["x"] + (1 if self._is_positive_sine else -1)
                y = ball["y"] + (1 if self._is_positive_cosine else -1)

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
                    ball["x"] = x
                    ball["y"] = y
                    continue

                # 他のボールとの衝突判定
                for index2, b in enumerate(self._balls[canvas_index]):
                    if index == index2:
                        continue
                    if b["x"] == x and b["y"] == y:
                        is_bottom_empty = False
                    if b["x"] == x and b["y"] == (
                        y - 1 if self._is_positive_cosine else y + 1
                    ):
                        is_bottom_right_empty = False
                    if (
                        b["x"] == (x - 1 if self._is_positive_sine else x + 1)
                        and b["y"] == y
                    ):
                        is_bottom_left_empty = False

                if not is_bottom_empty:
                    if is_bottom_right_empty:
                        y = y - 1 if self._is_positive_cosine else y + 1
                    elif is_bottom_left_empty:
                        x = x - 1 if self._is_positive_sine else x + 1
                    else:
                        y = y - 1 if self._is_positive_cosine else y + 1
                        x = x - 1 if self._is_positive_sine else x + 1

                ball["x"] = x
                ball["y"] = y

        return self._balls, self._angle, self._is_finish_falling

    def fall_dot(self, canvas_index: int) -> None:
        """
        ドットを落とす関数
        """
        x = 0 if self._is_positive_sine else GRID_SIZE - 1
        y = 0 if self._is_positive_cosine else GRID_SIZE - 1

        self._balls[canvas_index].append({"x": x, "y": y})

    def remove_dot(self, canvas_index: Optional[int] = None) -> bool:
        """ドットを削除する"""
        x = GRID_SIZE - 1 if self._is_positive_sine else 0
        y = GRID_SIZE - 1 if self._is_positive_cosine else 0
        if canvas_index is None:
            for i in range(len(self._balls)):
                index = self._find_index(
                    self._balls[i], lambda ball: ball["x"] == x and ball["y"] == y
                )
                if index == -1:
                    continue
                else:
                    del self._balls[i][index]
                    return True
            return False
        else:
            index = self._find_index(
                self._balls[canvas_index],
                lambda ball: ball["x"] == x and ball["y"] == y,
            )
            if index == -1:
                return False
            else:
                del self._balls[canvas_index][index]
                return True

    def set_angle(self) -> None:
        """角度を設定する"""
        self._angle += 90
        if self._angle > 180:
            self._angle -= 360
        self._is_finish_falling = False
        self._sound.stop()
        self._is_positive_sine = math.sin((self._angle * math.pi) / 180) >= 0
        self._is_positive_cosine = math.cos((self._angle * math.pi) / 180) >= 0

    def fall_dot_through_canvas(self) -> None:
        """キャンバスを通過してドットを落とす"""
        if math.tan((self._angle * math.pi) / 180) <= 0:
            self._sound.stop()
            return
        if math.tan((self._angle * math.pi) / 180) <= 0:
            self._is_finish_falling = False
            return

        # キャンバス通過：削除処理
        result = self.remove_dot(0 if self._is_positive_sine else 1)

        if result:
            # キャンバス通過：挿入処理（削除に成功時）
            self.fall_dot(1 if self._is_positive_sine else 0)
            self._is_finish_falling = False
        elif (
            not self._is_finish_falling
            and len(self._balls[0 if self._is_positive_sine else 1]) == 0
        ):
            # 既に全部通過済みの場合、１回だけ実行
            self._sound.play()
            self._is_finish_falling = True

    def _find_index(self, lst, predicate) -> int:
        for i, x in enumerate(lst):
            if predicate(x):
                return i
        return -1
