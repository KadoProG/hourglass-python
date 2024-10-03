import pygame
import sys

# 初期化
pygame.init()

# 画面のサイズを設定
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# アニメーション用の変数
x = 100  # オブジェクトの位置
y = 240
speed = 5
is_paused = False  # アニメーションが中断されているかどうかのフラグ

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# メインループ
while True:
    # イベント処理
    print("test")
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # "P"キーで中断・再開を切り替え
                is_paused = not is_paused

    # 中断されていない場合にアニメーションを進める
    if not is_paused:
        x += speed  # x方向に移動
        if x > 640:  # 画面を超えたら元に戻す
            x = 0

    # 画面を塗りつぶし
    screen.fill(WHITE)

    # オブジェクトを描画
    pygame.draw.circle(screen, RED, (x, y), 20)

    # 画面の更新
    pygame.display.flip()

    # フレームレートを設定（60FPS）
    clock.tick(60)
