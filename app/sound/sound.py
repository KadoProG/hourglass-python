from typing import Optional
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import curses
import os
import signal


class Sound:
    def __init__(self, stdscr: curses.window = None, is_init_play: bool = False):
        self._is_playing = False
        self.playback = None
        # M4Aファイルのロード
        self.sound = AudioSegment.from_file("cat-mean.m4a", format="m4a")

        # --------cursesの設定
        self._stdscr = stdscr
        if not stdscr is None:
            # 非エコーモードに設定
            curses.noecho()
            stdscr.nodelay(True)
            # 色の初期化 (赤色)
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            # キーボードショートカットを表示
            self._stdscr.addstr(0, 3, "[")
            self._stdscr.addstr("space", curses.color_pair(1))
            self._stdscr.addstr(f"]start/stop  [")
            self._stdscr.addstr("q", curses.color_pair(1))
            self._stdscr.addstr(f"]exit")
        if is_init_play:
            self.play()
        else:
            self.stop()

    def play(self):
        if self._is_playing:
            return
        self._is_playing = True
        self.playback = _play_with_simpleaudio(self.sound)
        self.stop_worker = self.playback.stop
        if not self._stdscr is None:
            self._stdscr.addstr(0, 0, "▶️")

    def stop(self):
        if not self._stdscr is None:
            self._stdscr.addstr(0, 0, "⏹")
        if self.playback and self._is_playing:
            self.stop_worker()
            self._is_playing = False

    def is_playing(self) -> bool:
        return self._is_playing

    def run(self, is_playing: Optional[bool] = None):
        self._stdscr.addstr(0, 4, "[space]再生/停止、[q]終了")
        if not is_playing is None and is_playing == True:
            self.play()
        while True:
            key = self._stdscr.getch()
            if key == ord(" "):
                if self._is_playing:
                    self.stop()
                else:
                    self.play()
            if key == ord("q"):
                os.kill(os.getpid(), signal.SIGINT)


def main(stdscr):
    sound = Sound(stdscr, True)

    try:
        while True:
            key = stdscr.getch()
            if key == ord(" "):
                if not sound.is_playing():
                    sound.play()
                else:
                    sound.stop()
            if key == ord("q"):
                sound.stop()
                break
    except KeyboardInterrupt:
        sound.stop()  # ctrl + C で終了時


if __name__ == "__main__":
    try:
        # cursesを使用するためのラッパー関数
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
