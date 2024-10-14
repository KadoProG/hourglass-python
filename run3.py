from app.config import FRAMERATE, GRID_SIZE
from app.hourglass.hourglass import HourGlass
import pygame
import sys

# 初期化
pygame.init()

# 画面のサイズを設定
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

radius = 20


# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def main():
    hourglass = HourGlass()

    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # "P"キーで中断・再開を切り替え
                    pass
                    # is_paused = not is_paused
        upperDots, lowerDots = hourglass.next_frame()
        # 画面を塗りつぶし
        screen.fill(WHITE)

        # オブジェクトを描画
        for dot in upperDots:
            pygame.draw.circle(
                screen, RED, (dot.x * radius, dot.y * radius), radius / 2
            )
        for dot in lowerDots:
            pygame.draw.circle(
                screen,
                RED,
                (
                    dot.x * radius + GRID_SIZE * radius,
                    dot.y * radius + GRID_SIZE * radius,
                ),
                radius / 2,
            )

        # 画面の更新
        pygame.display.flip()

        clock.tick(1 / FRAMERATE)


if __name__ == "__main__":
    main()
