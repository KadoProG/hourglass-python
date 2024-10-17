from app.config import FRAMERATE, INIT_ANGLE, GRID_SIZE
from app.hourglass.hourglass import HourGlass
from app.draws.draw_pygame import DrawPygame
from app.draws.draw_ledmatrix import DrawLedmatrix
from app.sound import sound as Sound
from app.events.pygame_keyevents import pygame_keyevents
from app.events.gpio_button import GpioButton
from app.utils.angle import Angle
from app.utils.pause import Pause
from app.utils.get_option import get_option
import math
from dotenv import load_dotenv
import os

load_dotenv()

boot = os.getenv("BOOT")
sensor = os.getenv("SENSOR")


def main():
    is_fixed = get_option()
    # ここで使用される変数の初期化
    angle = Angle(INIT_ANGLE, is_fixed)
    pre_is_finish_falling = True
    pause = Pause(False)
    is_positive_cosine = math.sin((angle() * math.pi) / 180) >= 0
    is_positive_sine = math.cos((angle() * math.pi) / 180) >= 0

    # インスタンスの生成
    hourglass = HourGlass(GRID_SIZE)
    drawPygame = DrawPygame(GRID_SIZE)
    drawLedmatrix = DrawLedmatrix(GRID_SIZE, FRAMERATE)
    sound = Sound()
    gpioButton = GpioButton()

    def start_stop():
        if pause():
            pause.set(False)
            if hourglass.get_is_finish_falling() and is_fixed:
                hourglass.reset()
        elif sound.is_playing():
            sound.stop()
            if is_fixed:
                pause.set(True)
        else:
            pause.set(True)

    while True:
        # キーイベントを取得
        pygame_keyevents(drawPygame, angle, start_stop)

        # ラズパイのセンサーがある場合はセンサーの値を取得
        if not is_fixed and boot == "raspberrypi" and sensor == "true":
            from app.events.mpu_events import get_mpu_angle

            roll, _ = get_mpu_angle()
            angle.set(-roll + 45)

        gpioButton.button_event(start_stop)

        # 角度を更新
        angle.next_frame()

        # 砂時計の角度を更新
        hourglass.set_angle(angle())

        # 次のアニメーションを描写
        if not pause():
            upperDots, lowerDots, is_finish_falling = hourglass.next_frame()

        # 砂時計が落ちきったらアラームを鳴らす
        if not pre_is_finish_falling and is_finish_falling:
            pre_is_finish_falling = True
            sound.play()
        elif not is_finish_falling:
            pre_is_finish_falling = False

        # 角度ジャッジが変化したらアラームを停止する
        pre_is_positive_sine = math.sin((angle() * math.pi) / 180) >= 0
        pre_is_positive_cosine = math.cos((angle() * math.pi) / 180) >= 0
        if not (
            pre_is_positive_cosine == is_positive_cosine
            and pre_is_positive_sine == is_positive_sine
        ):
            sound.stop()
            is_positive_sine = pre_is_positive_sine
            is_positive_cosine = pre_is_positive_cosine

        # 描写
        drawPygame.draw(upperDots, lowerDots, angle, sound.is_playing(), pause())
        drawLedmatrix.draw(upperDots, lowerDots, sound.is_playing())
        drawPygame.clock.tick(1 / FRAMERATE)


if __name__ == "__main__":
    main()
