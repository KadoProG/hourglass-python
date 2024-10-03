import os
import signal


def input_thread(stop_event, stdscr, draw, sandAnimation):
    """キー入力を処理する関数（無限ループ）"""
    while not stop_event.is_set():
        key = stdscr.getch()
        if key == ord("a"):
            sandAnimation.start_stop_click()
        if key == ord("r"):
            sandAnimation.set_angle()
        if key == ord("q"):
            os.kill(os.getpid(), signal.SIGINT)
        if key == ord("t"):
            draw.print_log("test")
