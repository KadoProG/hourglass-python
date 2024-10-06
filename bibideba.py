import RPi.GPIO as GPIO
import time
import curses
import threading


class Bibideba:
    def __init__(self, stdscr: curses.window = None, is_init_play: bool = False):
        # 設定
        BUZZER_PIN = 27  # GPIO 27(PIN 13)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
        self._buzzer = GPIO.PWM(BUZZER_PIN, 1)
        self._stop_flag = threading.Event()

        # --------cursesの設定
        self._stdscr = stdscr
        if not self._stdscr is None:
            # 非エコーモードに設定
            curses.noecho()
            self._stdscr.nodelay(True)
            # 色の初期化
            curses.start_color()
            curses.init_pair(
                1, curses.COLOR_RED, curses.COLOR_BLACK
            )  # カウンターの数字を赤色に設定

            # --------キーボードショートカットを表示
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
        if not self._stdscr is None:
            self._stdscr.addstr(0, 0, "▶️")
        self._stop_flag.clear()
        self._buzzer.start(50)
        play_thread = threading.Thread(target=self._play_song)
        play_thread.start()

    def stop(self):
        if not self._stdscr is None:
            self._stdscr.addstr(0, 0, "⏹")
        self._stop_flag.set()
        self._buzzer.stop()

    def is_playing(self) -> bool:
        return not self._stop_flag.is_set()

    def _play_song(self):
        while not self._stop_flag.is_set():
            self._play_bibideba_chorus_common()  # 繰り返し部分

            self._play_sound(320, 2, 0)  # 混（こん）
            self._play_sound(382, 1, 0)  # 絡（が）
            self._play_sound(430, 1, 0)  # （ら）
            self._play_sound(480, 2, 0)  # がっ
            self._play_sound(320, 1, 0)  # て
            self._play_sound(285, 1, 0)  # も
            self._play_sound(320, 2, 0)  # 仕様（しよう）
            self._play_sound(480, 3 / 3, 0)  # が
            self._play_sound(462, 1 / 3, 0)  #
            self._play_sound(480, 4 / 3, 0)  # ない
            self._play_sound(320, 1, 0)  # ガ
            self._play_sound(382, 1, 0)  # ラ
            self._play_sound(430, 1, 0)  # ス
            self._play_sound(480, 2, 0)  # シュー
            self._play_sound(320, 1, 0)  # ズ
            self._play_sound(285, 1, 0)  # で
            self._play_sound(320, 2, 0)  # お
            self._play_sound(480, 3 / 3, 0)  # とっ
            self._play_sound(462, 1 / 3, 0)  #
            self._play_sound(480, 8, 0)  # ない

            self._play_bibideba_chorus_common()  # 繰り返し部分

            self._play_sound(320, 2, 0)  # こん
            self._play_sound(382, 1, 0)  # や
            self._play_sound(430, 1, 0)  # に
            self._play_sound(480, 2, 0)  # あす
            self._play_sound(320, 1, 0)  # な
            self._play_sound(285, 1, 0)  # ど
            self._play_sound(320, 2, 0)  # な
            self._play_sound(620, 1 / 3, 0)  # ーい
            self._play_sound(660, 8 / 3, 0)  # ーい
            self._play_sound(462, 1, 0)  # な
            self._play_sound(430, 1, 0)  # ら
            self._play_sound(382, 1, 0)  # ば
            self._play_sound(430, 2, 0)  # 自由
            self._play_sound(382, 1, 0)  # に
            self._play_sound(430, 2, 0)  # 踊っ
            self._play_sound(382, 1, 0)  # た
            self._play_sound(430, 1, 0)  # も
            self._play_sound(382, 1, 0)  # ん
            self._play_sound(430, 1, 0)  # が
            self._play_sound(480, 3, 0)  # ち
            self._play_sound(285, 1, 0)  # で
            self._play_sound(320, 3, 0)  # しょ

    def _play_bibideba_chorus_common(self):
        self._play_sound(430, 1, 0)  # BI
        self._play_sound(480, 1, 0)  # BBI
        self._play_sound(430, 2, 0)  # DI

        self._play_sound(430, 1, 0)  # BO
        self._play_sound(480, 1, 0)  # BBI
        self._play_sound(430, 2, 0)  # DI
        self._play_sound(480, 3, 0)  # BOO
        self._play_sound(320, 3, 0)  # WA
        self._play_sound(430, 1, 0)  # BI
        self._play_sound(480, 1, 0)  # BBI
        self._play_sound(430, 1, 0)  # DI
        self._play_sound(480, 1, 0)  # BO
        self._play_sound(430, 1, 0)  # BBI
        self._play_sound(430, 1, 0)  # DI
        self._play_sound(480, 2, 0)  # BOO
        self._play_sound(320, 4, 0)  # BA
        self._play_sound(462, 2, 0)  # YEAH
        self._play_sound(430, 2, 0)  #
        self._play_sound(382, 2, 0)  #

    def _play_sound(self, tone: int, devide: float, pause: int):
        if self._stop_flag.is_set():
            return
        self._buzzer.ChangeFrequency(tone)
        time.sleep(devide * 0.127)
        if pause > 0:
            self._buzzer.stop()
            time.sleep(pause)


def main(stdscr: curses.window):
    bibideba = Bibideba(stdscr, True)

    try:
        while True:
            key = stdscr.getch()
            if key == ord(" "):
                if not bibideba.is_playing():
                    bibideba.play()
                else:
                    bibideba.stop()
            if key == ord("q"):
                bibideba.stop()
                break
    except KeyboardInterrupt:
        bibideba.stop()  # ctrl + C で終了時


if __name__ == "__main__":
    # cursesを使用するためのラッパー関数
    curses.wrapper(main)
