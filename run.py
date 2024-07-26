import signal
import os
import curses
import threading
from animation import (
    animation_routine,
    fall_ball,
    update_angle,
    fall_ball_throuth_canavs,
)
import time
from draw import draw_routine
from config import (
    grid_size,
    angle,
    animation_frame_time,
    interval_between_fall_time,
    interval_between_fall_throuth_time,
)

# ボールの数
ball_length = 60

interval_frequency = interval_between_fall_time / animation_frame_time
interval_canvas_frequency = interval_between_fall_throuth_time / animation_frame_time

canvas_frequency_temp = interval_frequency * ball_length + grid_size


def frame_routine_task_process(stdscr):
    global canvas_frequency_temp, interval_frequency, ball_length, interval_canvas_frequency
    # フレームを数えるだけ
    frame_count = 0

    # 投げたボールをカウント
    ball_count = 0

    draw_routine(stdscr, frame_count, ball_count, angle[0], curses)
    while True:
        animation_routine()
        frame_count = frame_count + 1
        draw_routine(stdscr, frame_count, ball_count, angle[0], curses)
        time.sleep(animation_frame_time)

        # 初期のボールを落とす
        if frame_count % interval_frequency == 0 and ball_count < ball_length:
            fall_ball(0)
            ball_count += 1

        # キャンバスを通過してボールを落とす
        if (
            canvas_frequency_temp < frame_count
            and frame_count % interval_canvas_frequency == 0
        ):
            fall_ball_throuth_canavs()


# キー入力を処理する関数
def input_thread(stop_event, stdscr):
    while not stop_event.is_set():
        key = stdscr.getch()
        if key == ord("a"):
            update_angle()
        if key == ord("q"):
            os.kill(os.getpid(), signal.SIGINT)


def main(stdscr):
    # 非エコーモードに設定
    curses.noecho()
    stdscr.nodelay(True)

    # 停止イベントを作成
    stop_event = threading.Event()

    # 色の初期化
    curses.start_color()
    curses.init_pair(
        1, curses.COLOR_RED, curses.COLOR_BLACK
    )  # カウンターの数字を赤色に設定

    # 入力スレッドを開始
    input_thread_obj = threading.Thread(
        target=input_thread, args=(stop_event, stdscr), daemon=True
    )
    input_thread_obj.start()

    # メイン処理を実行
    frame_routine_task_process(stdscr)

    # 入力スレッドが終了するのを待機
    input_thread_obj.join()


if __name__ == "__main__":
    try:
        # cursesを使用するためのラッパー関数
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
