from src.config import (
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
from src.events.input_changes import input_thread
from src.draw import Draw
from src.sand_animation import SandAnimation
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

boot = os.getenv("BOOT")


def frame_routine_task_process(
    draw: Draw, sandAnimation: SandAnimation, is_fixed: bool
):
    """フレーム単位で無限ループの処理を実行する関数"""
    interval_frequency = INTERVAL_FALLING / FRAMERATE
    interval_canvas_frequency = INTERVAL_THROUTH_CANVAS / FRAMERATE
    canvas_frequency_temp = interval_frequency * BALL_LENGTH + GRID_SIZE

    # フレームを数えるだけ
    frame_count = 0

    # 投げたボールをカウント
    ball_count = 0

    draw.draw_frame([[], []], INIT_ANGLE, False, frame_count)

    balls = [[], []]
    angle = INIT_ANGLE
    is_finish_falling = False

    while True:
        time.sleep(FRAMERATE)
        if not is_fixed and boot == "raspberrypi":
            from src.events.mpu_events import get_mpu_angle

            roll, _ = get_mpu_angle()
            sandAnimation.set_angle(-roll + 45)

        if sandAnimation.is_paused:
            draw.draw_frame(
                balls, angle, sandAnimation._sound.is_playing(), frame_count, True
            )
            continue
        balls, angle, is_finish_falling = sandAnimation.next_frame()
        draw.draw_frame(balls, angle, is_finish_falling, frame_count)
        frame_count += 1

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", help="optional", action="store_true")
    args = parser.parse_args()

    is_fixed = args.fix

    # 停止イベントを作成
    stop_event = threading.Event()

    # 描画クラスを作成
    draw = Draw(stdscr, is_fixed)
    sound = None

    if boot == "raspberrypi":
        from src.sound.bibideba import Bibideba

        sound = Bibideba()
    elif boot == "macos":
        from src.sound.sound import Sound

        sound = Sound()

    else:
        from src.sound.sound_mock import SoundMock

        sound = SoundMock()

    sandAnimation = SandAnimation(sound, is_fixed)

    if boot == "raspberrypi":
        from src.events.button import button_thread

        button_thread_obj = threading.Thread(
            target=button_thread,
            args=(stop_event, sandAnimation.start_stop_click),
            daemon=True,
        )
        # 入力スレッドを開始
        button_thread_obj.start()

    input_thread_obj = threading.Thread(
        target=input_thread, args=(stop_event, stdscr, draw, sandAnimation), daemon=True
    )

    # 入力スレッドを開始
    input_thread_obj.start()

    # メイン処理を実行
    frame_routine_task_process(draw, sandAnimation, is_fixed)


if __name__ == "__main__":
    try:
        # cursesを使用するためのラッパー関数
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
