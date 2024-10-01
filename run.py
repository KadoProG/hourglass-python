from config import (
    GRID_SIZE,
    FRAMERATE,
    INTERVAL_FALLING,
    INTERVAL_THROUTH_CANVAS,
    BALL_LENGTH,
    INIT_ANGLE,
)
import curses
import threading
import time
from input_changes import input_thread
from draw import Draw
from sand_animation import SandAnimation


interval_frequency = INTERVAL_FALLING / FRAMERATE
interval_canvas_frequency = INTERVAL_THROUTH_CANVAS / FRAMERATE

canvas_frequency_temp = interval_frequency * BALL_LENGTH + GRID_SIZE


def frame_routine_task_process(draw: Draw, sandAnimation: SandAnimation):
    """フレーム単位で無限ループの処理を実行する関数"""
    global canvas_frequency_temp, interval_frequency, interval_canvas_frequency
    # フレームを数えるだけ
    frame_count = 0

    # 投げたボールをカウント
    ball_count = 0

    draw.draw_frame([[], []], INIT_ANGLE, False, frame_count, ball_count)

    while True:
        balls, angle, is_finish_falling = sandAnimation.next_frame()
        draw.draw_frame(balls, angle, is_finish_falling, frame_count, ball_count)
        frame_count += 1
        time.sleep(FRAMERATE)

        # 初期のボールを落とす
        if frame_count % interval_frequency == 0 and ball_count < BALL_LENGTH:
            sandAnimation.fall_dot(0)
            ball_count += 1

        # キャンバスを通過してボールを落とす
        if (
            canvas_frequency_temp < frame_count
            and frame_count % interval_canvas_frequency == 0
        ):
            sandAnimation.fall_dot_through_canvas()


def main(stdscr: curses.window):
    # 描画クラスを作成
    draw = Draw(stdscr)
    sandAnimation = SandAnimation(draw)

    # 停止イベントを作成
    stop_event = threading.Event()

    input_thread_obj = threading.Thread(
        target=input_thread, args=(stop_event, stdscr, draw, sandAnimation), daemon=True
    )

    # 入力スレッドを開始
    input_thread_obj.start()

    # メイン処理を実行
    frame_routine_task_process(draw, sandAnimation)


if __name__ == "__main__":
    try:
        # cursesを使用するためのラッパー関数
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
