from dotenv import load_dotenv
import os

# GPIOモジュールの設定
# GPIO.setmode(GPIO.BCM)  # または GPIO.BOARD
# もう片方は3.3vへ

BUTTON = 25  # 使用するGPIOピン番号 pin22

load_dotenv()
boot = os.getenv("BOOT")


class GpioButton:
    def __init__(self):
        self.__pre_value = 0
        self.__GPIO = None
        if boot != "raspberrypi":
            return

        import RPi.GPIO as GPIO

        GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.__GPIO = GPIO

    def button_event(self, start_stop):
        if self.__GPIO is None:
            return
        btn = self.__GPIO.input(BUTTON)
        if btn == 1 and self.__pre_value == 0:
            start_stop()
            self.__pre_value = 1
        if btn == 0:
            self.__pre_value = 0
