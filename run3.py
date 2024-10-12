from app.config import FRAMERATE
from app.hourglass.hourglass import HourGlass
import time


def main():
    hourglass = HourGlass()

    while True:
        time.sleep(FRAMERATE)
        hourglass.next_frame()

if __name__ == "__main__":
    main()
