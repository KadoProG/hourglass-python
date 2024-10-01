import os
import signal
from animation import update_angle


def input_thread(stop_event, stdscr, draw):
    """キー入力を処理する関数（無限ループ）"""
    while not stop_event.is_set():
        key = stdscr.getch()
        if key == ord("a"):
            update_angle()
        if key == ord("q"):
            os.kill(os.getpid(), signal.SIGINT)
        if key == ord("t"):
            draw.print_log("test")
