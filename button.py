import RPi.GPIO as GPIO
import time

# GPIOモジュールの設定
# GPIO.setmode(GPIO.BCM)  # または GPIO.BOARD
# もう片方は3.3vへ

BUTTON = 25  # 使用するGPIOピン番号 pin22

# GPIOピンの設定
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# メインループ
def button_thread(stop_event, start_stop_click):
    try:
        pre_btn = 0
        while not stop_event.is_set():
            time.sleep(0.1)
            btn = GPIO.input(BUTTON)
            if btn == 1 and pre_btn == 0:
                start_stop_click()
                pre_btn = 1
            if btn == 0:
              pre_btn = 0
    except KeyboardInterrupt:
        print("Exiting...")
