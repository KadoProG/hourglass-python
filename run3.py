from app.config import FRAMERATE, INIT_ANGLE
from app.hourglass.hourglass import HourGlass
from app.draws.draw_pygame import DrawPygame
from app.sound import sound as Sound
import pygame
import sys
import math
from dotenv import load_dotenv
import os

load_dotenv()

boot = os.getenv("BOOT")
sensor = os.getenv("SENSOR")


def main():
    is_fixed = False
    # ここで使用される変数の初期化
    angle = INIT_ANGLE
    pre_is_finish_falling = True
    is_paused = False
    is_positive_cosine = math.sin((angle * math.pi) / 180) >= 0
    is_positive_sine = math.cos((angle * math.pi) / 180) >= 0
    auto_rotation = 0

    # インスタンスの生成
    hourglass = HourGlass()
    drawPygame = DrawPygame()
    sound = Sound()
    upperDots, lowerDots = [], []

    while True:
        # イベント処理
        for event in drawPygame.event().get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_a:
                    if is_paused:
                        is_paused = False
                    elif sound.is_playing():
                        sound.stop()
                    else:
                        is_paused = True
                    sound.stop()
                elif event.key == pygame.K_w:
                    auto_rotation -= 1
                elif event.key == pygame.K_e:
                    angle -= 90
                elif event.key == pygame.K_t:
                    auto_rotation += 1
                elif event.key == pygame.K_r:
                    angle += 90
            elif event.type == pygame.VIDEORESIZE:
                drawPygame.video_resize(event)

        # ラズパイのセンサーがある場合はセンサーの値を取得
        if not is_fixed and boot == "raspberrypi" and sensor == "true":
            from app.events.mpu_events import get_mpu_angle

            roll, _ = get_mpu_angle()
            angle = -roll + 45

        # 角度を更新
        angle += auto_rotation**2 * (-1 if auto_rotation < 0 else 1)

        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360

        # 砂時計の角度を更新
        hourglass.set_angle(angle)

        # 次のアニメーションを描写
        if not is_paused:
            upperDots, lowerDots, is_finish_falling = hourglass.next_frame()

        # 砂時計が落ちきったらアラームを鳴らす
        if not pre_is_finish_falling and is_finish_falling:
            pre_is_finish_falling = True
            sound.play()
        elif not is_finish_falling:
            pre_is_finish_falling = False

        # 角度ジャッジが変化したらアラームを停止する
        pre_is_positive_sine = math.sin((angle * math.pi) / 180) >= 0
        pre_is_positive_cosine = math.cos((angle * math.pi) / 180) >= 0
        if not (
            pre_is_positive_cosine == is_positive_cosine
            and pre_is_positive_sine == is_positive_sine
        ):
            sound.stop()
            is_positive_sine = pre_is_positive_sine
            is_positive_cosine = pre_is_positive_cosine

        # 描写
        drawPygame.draw(
            upperDots, lowerDots, angle, sound.is_playing(), auto_rotation, is_paused
        )
        drawPygame.clock.tick(1 / FRAMERATE)


if __name__ == "__main__":
    main()
