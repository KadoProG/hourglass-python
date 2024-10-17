from app.hourglass.dot import Dot
from app.utils.angle import Angle
from dotenv import load_dotenv
import os


load_dotenv()
boot = os.getenv("BOOT")


class DrawLedmatrix:
    def __init__(self, grid_size: int, framerate: int):
        self.__grid_size = grid_size
        self.__framerate = framerate
        self.__device = None
        self.__canvas = None

        self.__outer_chamber = []
        self.__count_led_frame = 0

        if boot == "raspberrypi":
            from luma.core.interface.serial import spi, noop
            from luma.core.render import canvas
            from luma.led_matrix.device import max7219

            # 初期設定
            serial = spi(port=0, device=0, gpio=noop())
            self.__device = max7219(serial, cascaded=2, block_orientation=90, rotate=0)
            self.__canvas = canvas

            # 上と下の外周を格納
            for x in range(grid_size):
                self.__outer_chamber.append(Dot(x, 0))  # 上端
                self.__outer_chamber.append(Dot(x, grid_size - 1))  # 下端
                self.__outer_chamber.append(Dot(0, x))  # 左端
                self.__outer_chamber.append(Dot(grid_size - 1, x))  # 右端

    def draw(self, upper_dots, lower_dots, is_alerm: bool):
        if is_alerm:
            self.__count_led_frame += 1
            if (
                self.__count_led_frame > 0
                and self.__count_led_frame < 1 / self.__framerate / 2
            ):
                upper_dots = self.__outer_chamber
                lower_dots = self.__outer_chamber
            elif not self.__count_led_frame < 1 / self.__framerate / 2:
                self.__count_led_frame = -1 / self.__framerate / 2

        if not self.__device is None and not self.__canvas is None:
            with self.__canvas(self.__device) as draw:
                for index, ball_items in enumerate([upper_dots, lower_dots]):
                    for ball in ball_items:
                        x = ball.x
                        y = ball.y
                        if index == 1:
                            x += self.__grid_size
                        draw.point((x, y), fill="white")  # 点灯するドットを描画
