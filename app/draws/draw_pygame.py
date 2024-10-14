from app.config import GRID_SIZE
import pygame


# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (200, 255, 200)


class DrawPygame:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()  # ディスプレイ情報を取得
        self.x, self.y = info.current_w / 2, info.current_h
        self.screen = pygame.display.set_mode((self.x, self.y), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        screen_radius = min(self.x, self.y) // 2
        self.radius = screen_radius / GRID_SIZE // 2
        # 仮想キャンバスの作成
        canvas_size = (self.radius * GRID_SIZE * 2, self.radius * GRID_SIZE * 2)
        self.chamba_size = GRID_SIZE * self.radius
        self.canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)

    def draw(self, upper_dots, lower_dots, angle: int, is_alerm: bool):
        # オブジェクトを描画
        pygame.draw.rect(self.canvas, GREEN, (0, 0, self.chamba_size, self.chamba_size))

        for dot in upper_dots:
            x = dot.x * self.radius + self.radius / 2
            y = dot.y * self.radius + self.radius / 2
            pygame.draw.circle(self.canvas, RED, (x, y), self.radius / 2)

        pygame.draw.rect(
            self.canvas,
            GREEN,
            (  # 二個目の砂時計ボックスの位置
                self.chamba_size,
                self.chamba_size,
                self.chamba_size,
                self.chamba_size,
            ),
        )

        for dot in lower_dots:
            pygame.draw.circle(
                self.canvas,
                RED,
                (
                    dot.x * self.radius + self.chamba_size + self.radius / 2,
                    dot.y * self.radius + self.chamba_size + self.radius / 2,
                ),
                self.radius / 2,
            )

        # キャンバスの回転
        rotated_canvas = pygame.transform.rotate(self.canvas, -angle)
        rect = rotated_canvas.get_rect(
            center=(self.x / 2, self.y / 2)
        )  # メイン画面中央に配置
        # 画面を塗りつぶし
        self.screen.fill(WHITE)
        # メイン画面の更新
        self.screen.blit(rotated_canvas, rect)  # 回転したキャンバスをメイン画面に描画

        # フォントの設定
        font = pygame.font.Font(None, 18)  # デフォルトフォント（サイズ36）
        # テキストの設定
        text = "[a]Start/Stop [t]Auto Rotation [r]Custom Rotation [q]Quit"
        text_color = (0, 0, 0)  # 黒色
        text_image = font.render(text, True, text_color)
        self.screen.blit(text_image, (20, 20))

        if is_alerm:
            # フォントの設定
            font = pygame.font.Font(None, 36)  # デフォルトフォント（サイズ36）
            # テキストの設定
            text = "Hello, Pygame!"
            text_color = (0, 0, 0)  # 黒色
            text_image = font.render(text, True, text_color)
            self.screen.blit(text_image, (50, 50))

        pygame.display.flip()  # 画面の更新
        self.clock.tick(60)

    def video_resize(self, event):
        self.x, self.y = event.w, event.h
        self.screen = pygame.display.set_mode((self.x, self.y), pygame.RESIZABLE)
        screen_radius = min(self.x, self.y) // 2
        self.radius = screen_radius / GRID_SIZE // 2
        # 仮想キャンバスの作成
        canvas_size = (self.radius * GRID_SIZE * 2, self.radius * GRID_SIZE * 2)
        self.chamba_size = GRID_SIZE * self.radius
        self.canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)

    def event(self):
        return pygame.event

    def clock(self):
        return self.clock
