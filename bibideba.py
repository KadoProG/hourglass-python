# ======== ビビデバ =========== 星街すいせい ==========
# ======== GPIOポートに接続したスピーカーを鳴らす ========
import RPi.GPIO as GPIO
import time
import threading

# 設定
BUZZER_PIN = 27  # GPIO 27(PIN 13)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

buzzer = GPIO.PWM(BUZZER_PIN, 1)
stop_flag = threading.Event()
pause_flag = threading.Event()


def play_sound(tone: int, devide: float, pause: int):
    if stop_flag.is_set():
        return
    buzzer.ChangeFrequency(tone)
    time.sleep(devide * 0.127)
    if pause > 0:
        buzzer.stop()
        time.sleep(pause)


# ここから音程を刻み込む
buzzer.start(50)


def play_bibideba_chorus_common():
    play_sound(430, 1, 0)  # BI
    play_sound(480, 1, 0)  # BBI
    play_sound(430, 2, 0)  # DI

    play_sound(430, 1, 0)  # BO
    play_sound(480, 1, 0)  # BBI
    play_sound(430, 2, 0)  # DI
    play_sound(480, 3, 0)  # BOO
    play_sound(320, 3, 0)  # WA
    play_sound(430, 1, 0)  # BI
    play_sound(480, 1, 0)  # BBI
    play_sound(430, 1, 0)  # DI
    play_sound(480, 1, 0)  # BO
    play_sound(430, 1, 0)  # BBI
    play_sound(430, 1, 0)  # DI
    play_sound(480, 2, 0)  # BOO
    play_sound(320, 4, 0)  # BA
    play_sound(462, 2, 0)  # YEAH
    play_sound(430, 2, 0)  #
    play_sound(382, 2, 0)  #


def play_song():
    while not stop_flag.is_set():
        play_bibideba_chorus_common()  # 繰り返し部分

        play_sound(320, 2, 0)  # 混（こん）
        play_sound(382, 1, 0)  # 絡（が）
        play_sound(430, 1, 0)  # （ら）
        play_sound(480, 2, 0)  # がっ
        play_sound(320, 1, 0)  # て
        play_sound(285, 1, 0)  # も
        play_sound(320, 2, 0)  # 仕様（しよう）
        play_sound(480, 3 / 3, 0)  # が
        play_sound(462, 1 / 3, 0)  #
        play_sound(480, 4 / 3, 0)  # ない
        play_sound(320, 1, 0)  # ガ
        play_sound(382, 1, 0)  # ラ
        play_sound(430, 1, 0)  # ス
        play_sound(480, 2, 0)  # シュー
        play_sound(320, 1, 0)  # ズ
        play_sound(285, 1, 0)  # で
        play_sound(320, 2, 0)  # お
        play_sound(480, 3 / 3, 0)  # とっ
        play_sound(462, 1 / 3, 0)  #
        play_sound(480, 8, 0)  # ない

        play_bibideba_chorus_common()  # 繰り返し部分

        play_sound(320, 2, 0)  # こん
        play_sound(382, 1, 0)  # や
        play_sound(430, 1, 0)  # に
        play_sound(480, 2, 0)  # あす
        play_sound(320, 1, 0)  # な
        play_sound(285, 1, 0)  # ど
        play_sound(320, 2, 0)  # な
        play_sound(620, 1 / 3, 0)  # ーい
        play_sound(660, 8 / 3, 0)  # ーい
        play_sound(462, 1, 0)  # な
        play_sound(430, 1, 0)  # ら
        play_sound(382, 1, 0)  # ば
        play_sound(430, 2, 0)  # 自由
        play_sound(382, 1, 0)  # に
        play_sound(430, 2, 0)  # 踊っ
        play_sound(382, 1, 0)  # た
        play_sound(430, 1, 0)  # も
        play_sound(382, 1, 0)  # ん
        play_sound(430, 1, 0)  # が
        play_sound(480, 3, 0)  # ち
        play_sound(285, 1, 0)  # で
        play_sound(320, 3, 0)  # しょ


def start_playing():
    stop_flag.clear()
    song_thread = threading.Thread(target=play_song)
    song_thread.start()


def stop_playing():
    stop_flag.set()


def main():
    try:
        start_playing()
        while True:
            command = (
                input("Enter 's' to stop, 'r' to resume, 'q' to quit: ").strip().lower()
            )
            if command == "s":
                stop_playing()
            elif command == "r":
                start_playing()
            elif command == "q":
                stop_playing()
                break
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
