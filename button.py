import RPi.GPIO as GPIO
import time

# GPIOモジュールの設定
# GPIO.setmode(GPIO.BCM)  # または GPIO.BOARD

BUTTON = 25  # 使用するGPIOピン番号

# GPIOピンの設定
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# メインループ
def button_thread(stop_event, bibideba):
    try:
        while not stop_event.is_set():
            time.sleep(0.1)
            btn = GPIO.input(BUTTON)
            if btn == 1:
                bibideba.stop_playing()
    except KeyboardInterrupt:
        print("Exiting...")
