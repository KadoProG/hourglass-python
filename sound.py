from typing import Optional
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import curses
import os
import signal


class Sound:
    def __init__(self, stdscr: curses.window = None):
        # M4Aファイルのロード
        self.stdscr = stdscr
        if not stdscr is None:
            self.stdscr.addstr(0, 0, "⏹")
        self.is_playing = False
        self.playback = None
        self.sound = AudioSegment.from_file("cat-mean.m4a", format="m4a")

    def play(self):
        if self.is_playing:
            return
        self.is_playing = True
        self.playback = _play_with_simpleaudio(self.sound)
        self.stop_worker = self.playback.stop
        if not self.stdscr is None:
            self.stdscr.addstr(0, 0, "▶️")

    def stop(self):
        if self.playback and self.is_playing:
            self.stop_worker()
            self.is_playing = False
            if not self.stdscr is None:
                self.stdscr.addstr(0, 0, "⏹")

    def run(self, is_playing: Optional[bool] = None):
        self.stdscr.addstr(0, 4, "[space]再生/停止、[q]終了")
        if not is_playing is None and is_playing == True:
            self.play()
        while True:
            key = self.stdscr.getch()
            if key == ord(" "):
                if self.is_playing:
                    self.stop()
                else:
                    self.play()
            if key == ord("q"):
                os.kill(os.getpid(), signal.SIGINT)


def main(stdscr):
    # 非エコーモードに設定
    curses.noecho()
    stdscr.nodelay(True)

    sound = Sound(stdscr)
    sound.run(True)


if __name__ == "__main__":
    try:
        # cursesを使用するためのラッパー関数
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
