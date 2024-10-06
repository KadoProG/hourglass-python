from config import GRID_SIZE, FRAMERATE, INIT_ANGLE
import curses
import math


class Draw:
    """
    描画を行うクラス

    Attributes
    ----------
    _grid : list
        空のグリッド
    _logs : list
        ログのリスト
    _count_angle_diff_frame : float
        角度が変わるときのフレーム数
    _pre_angle : int
        前の角度
    """

    _grid = [["◯" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    _logs = []
    _count_angle_diff_frame = 1 / FRAMERATE
    _pre_angle = INIT_ANGLE
    _is_fixed = False

    def __init__(
        self, stdscr: curses.window, boot: str, is_fixed: bool = False
    ) -> None:
        self._stdscr = stdscr
        # 非エコーモードに設定
        curses.noecho()
        self._stdscr.nodelay(True)

        # 色の初期化
        curses.start_color()
        curses.init_pair(
            1, curses.COLOR_RED, curses.COLOR_BLACK
        )  # カウンターの数字を赤色に設定

        self._is_fixed = is_fixed

        # --------ラズベリーパイ仕様のモードではGPIO関連を読み込む
        self._device = None
        self._canvas = None
        if boot == "raspberrypi":
            # 1. **VCC** - 5V（ピン2または4）
            # 2. **GND** - GND（ピン6、9、14、20、25、30、34、39のいずれか）
            # 3. **DIN** - MOSI（ピン19）
            # 4. **CS** - CE0（ピン24）
            # 5. **CLK** - SCLK（ピン23）

            from luma.core.interface.serial import spi, noop
            from luma.core.render import canvas
            from luma.led_matrix.device import max7219

            # 初期設定
            serial = spi(port=0, device=0, gpio=noop())
            self._device = max7219(serial, cascaded=2, block_orientation=90, rotate=0)
            self._canvas = canvas

    def draw_frame(
        self,
        balls: list[list[dict[str, int]]],
        angle: int,
        is_finish_falling: bool,
        frame_count: int,
        is_paused: bool = False,
    ) -> None:
        self._stdscr.clear()
        # 空のグリッドを作成
        self._grid = [["◯" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE * 2)]

        self._draw_grid(balls[0], 0)
        self._draw_grid(balls[1], 1)

        # --------１行目のメッセージ
        row0_message = (
            f"frame: {frame_count:> 5} angle: {angle:> 4}° GRID_SIZE: {GRID_SIZE:< 3}"
        )
        self._stdscr.addstr(0, 0, row0_message)

        # --------２行目のメッセージ
        if self._pre_angle != angle or self._count_angle_diff_frame < 1 / FRAMERATE:
            if self._pre_angle != angle:
                self._pre_angle = angle
                self._count_angle_diff_frame = 0
            self._stdscr.addstr(1, 4, "[")
            self._stdscr.addstr("event", curses.color_pair(1))
            self._stdscr.addstr(f"] angleを{angle:> 4}° に変更")
            self._count_angle_diff_frame += 1

        if is_paused:
            self._stdscr.addstr(1, 4, "[")
            self._stdscr.addstr("pause", curses.color_pair(1))
            self._stdscr.addstr("]")

        # --------グリッドを描写
        for index, row in enumerate(self._grid):
            row_text = ("  " * GRID_SIZE if index >= GRID_SIZE else "") + " ".join(row)
            self._stdscr.addstr(index + 2, 2, row_text)

        if not self._device is None and not self._canvas is None:
            with self._canvas(self._device) as draw:
                for index, ball_items in enumerate(balls):
                    for ball in ball_items:
                        x = ball["x"]
                        y = ball["y"]
                        if index == 1:
                            x += GRID_SIZE
                        draw.point((x, y), fill="white")  # 点灯するドットを描画

        # --------これは数字を表示するための行
        row_text = ("").join([f"{i:> 2}" for i in range(GRID_SIZE)])[1:]
        self._stdscr.addstr(
            GRID_SIZE * 2 + 2, 0 + 2, f"{row_text} {row_text}", curses.color_pair(1)
        )

        # --------これは数字を表示するための列
        for index in range(GRID_SIZE * 2):
            self._stdscr.addstr(
                index + 2, GRID_SIZE * 4 + 1, f"{index:> 2}", curses.color_pair(1)
            )

        # --------キーボードショートカットを表示
        self._stdscr.addstr(GRID_SIZE * 2 + 3, 1, "[")
        self._stdscr.addstr("a", curses.color_pair(1))
        self._stdscr.addstr(f"]start/stop  [")
        if not self._is_fixed:
            self._stdscr.addstr("r", curses.color_pair(1))
            self._stdscr.addstr(f"]rotate  [")
        self._stdscr.addstr("t", curses.color_pair(1))
        self._stdscr.addstr(f"]log  [")
        self._stdscr.addstr("q", curses.color_pair(1))
        self._stdscr.addstr(f"]exit")

        # --------ログを表示
        for index, log in enumerate(self._logs):
            self._stdscr.addstr(GRID_SIZE * 2 + 4 + index, 0, "[")
            self._stdscr.addstr(str(index + 1), curses.color_pair(1))
            self._stdscr.addstr(f"]{log}")

        # --------アラームを表示
        if is_finish_falling:
            self._stdscr.addstr(1, GRID_SIZE * 4 + 4, "Alerm!")

        # --------角度に応じて星を描写
        is_positive_sine = math.sin((angle * math.pi) / 180) >= 0
        is_positive_cosine = math.cos((angle * math.pi) / 180) >= 0

        self._stdscr.addstr(
            (GRID_SIZE * 2 + 2 if is_positive_cosine else 1),
            (GRID_SIZE * 4 + 2 if is_positive_sine else 0),
            "☆",
        )

    def _draw_grid(self, balls, index: int) -> None:
        """balls配列に基づいてドットを配置"""
        for ball in balls:
            x, y = ball["x"], ball["y"]
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                self._grid[y + index * GRID_SIZE][x] = "●"

    def print_log(self, message: str) -> None:
        """ログを表示する"""
        self._logs.append(message)
