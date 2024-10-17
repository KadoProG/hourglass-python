import math
from app.config import (
    FRAMERATE,
    INIT_ANGLE,
    INTERVAL_FALLING,
    BALL_LENGTH,
    INTERVAL_THROUTH_CANVAS,
)
from app.hourglass.chamber import Chamber


class HourGlass:
    def __init__(self, grid_size: int) -> None:
        self.upper_chamber = Chamber(grid_size)
        self.lower_chamber = Chamber(grid_size)
        self._angle = INIT_ANGLE
        self._frame_count = 0
        """フレームを数える"""
        self._ball_count = 0
        """投げたボールをカウント"""
        self._is_finish_falling = True

        self._interval_frequency = INTERVAL_FALLING / FRAMERATE
        self._interval_canvas_frequency = INTERVAL_THROUTH_CANVAS / FRAMERATE
        self._canvas_frequency_temp = self._interval_frequency * BALL_LENGTH + grid_size

    def next_frame(self):
        self.upper_chamber.next_frame(self._angle)
        self.lower_chamber.next_frame(self._angle)
        # 初期のボールを落とす
        if (
            self._frame_count % self._interval_frequency == 0
            and self._ball_count < BALL_LENGTH
        ):
            self.upper_chamber.add_dot(self._angle)
            self._ball_count += 1
        self._frame_count += 1
        # キャンバスを通過してボールを落とす
        if (
            self._canvas_frequency_temp < self._frame_count
            and self._frame_count % self._interval_canvas_frequency == 0
        ):
            self.pass_canvas()

        return self.upper_chamber.dots, self.lower_chamber.dots, self._is_finish_falling

    def pass_canvas(self):
        """キャンバスを通過してボールを落とす"""
        if math.tan((self._angle * math.pi) / 180) <= 0:
            return

        is_positive_sine = math.sin((self._angle * math.pi) / 180) >= 0

        # キャンバス通過：削除処理
        result = (
            self.upper_chamber.remove_dot()
            if is_positive_sine
            else self.lower_chamber.remove_dot()
        )

        if result:
            # キャンバス通過：挿入処理（削除に成功時）
            (
                self.lower_chamber.add_dot(self._angle)
                if is_positive_sine
                else self.upper_chamber.add_dot(self._angle)
            )
            self._is_finish_falling = False  # 通過したので、フラグを戻す
        elif (
            not self._is_finish_falling
            and len(
                self.upper_chamber.dots if is_positive_sine else self.lower_chamber.dots
            )
            == 0
        ):
            self._is_finish_falling = True
            # 既に全部通過済みの場合、１回だけ実行

    def set_angle(self, angle: int = None) -> None:
        """角度を設定する"""
        if angle is None:
            self._angle += 90
        else:
            self._angle = angle

        if self._angle > 180:
            self._angle -= 360

    def get_is_finish_falling(self) -> bool:
        return self._is_finish_falling

    def reset(self, ball_length: int = None) -> None:
        length = self.lower_chamber.remove_all()
        if ball_length is not None:
            self.upper_chamber.remove_all()
            length = ball_length

        for _ in range(length):
            self.upper_chamber.add_dot(self._angle)
