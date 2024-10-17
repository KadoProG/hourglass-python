from app.draws.draw_pygame import DrawPygame
from app.utils.angle import Angle
from app.utils.pause import Pause
import pygame
import sys


def pygame_keyevents(drawPygame: DrawPygame, sound, angle: Angle, pause: Pause):
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
                elif sound.is_playing():
                    sound.stop()
                else:
                    pause.set(True)
                sound.stop()
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
