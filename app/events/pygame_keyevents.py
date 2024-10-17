from app.draws.draw_pygame import DrawPygame
from app.hourglass.hourglass import HourGlass
from app.utils.angle import Angle
from app.utils.pause import Pause
import pygame
import sys


def pygame_keyevents(
    drawPygame: DrawPygame,
    sound,
    angle: Angle,
    pause: Pause,
    hourglass: HourGlass,
    is_fixed: bool,
):
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
            elif event.key == pygame.K_w:
                angle.set_auto_rotation(-1)
            elif event.key == pygame.K_e:
                angle.set(angle() - 90)
            elif event.key == pygame.K_r:
                angle.set(angle() + 90)
            elif event.key == pygame.K_t:
                angle.set_auto_rotation(1)
        elif event.type == pygame.VIDEORESIZE:
            drawPygame.video_resize(event)
