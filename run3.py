from app.config import FRAMERATE, GRID_SIZE, INIT_ANGLE
from app.hourglass.hourglass import HourGlass
from app.draws.draw_pygame import DrawPygame
import pygame
import sys


def main():
    hourglass = HourGlass()

    # 回転角度
    angle = INIT_ANGLE
    pre_is_finish_falling = True
    is_alerm = False
    is_auto_rotation = False

    drawPygame = DrawPygame()

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
                    is_alerm = False
                elif event.key == pygame.K_t:
                    is_auto_rotation = not is_auto_rotation
                elif event.key == pygame.K_r:
                    angle += 90
            elif event.type == pygame.VIDEORESIZE:
                drawPygame.video_resize(event)

        # 角度を増加させる
        if is_auto_rotation:
            angle += 1  # 毎フレーム1度回転

        if angle < -360:
            angle = 0

        # 砂時計の角度を更新
        hourglass.set_angle(angle)

        # 次のアニメーションを描写
        upperDots, lowerDots, is_finish_falling = hourglass.next_frame()

        # 砂時計が落ちきったらアラームを鳴らす
        if not pre_is_finish_falling and is_finish_falling:
            is_alerm = True
            pre_is_finish_falling = True
        elif not is_finish_falling:
            is_alerm = False
            pre_is_finish_falling = False

        # 描写
        drawPygame.draw(upperDots, lowerDots, angle, is_alerm)
        drawPygame.clock.tick(1 / FRAMERATE)


if __name__ == "__main__":
    main()
