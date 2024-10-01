from config import GRID_SIZE, FRAMERATE, INIT_ANGLE, balls, is_finish_falling, angle
import curses


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

    def __init__(self, stdscr):
        self._stdscr = stdscr
        # 非エコーモードに設定
        curses.noecho()
        self._stdscr.nodelay(True)

        # 色の初期化
        curses.start_color()
        curses.init_pair(
            1, curses.COLOR_RED, curses.COLOR_BLACK
        )  # カウンターの数字を赤色に設定

    def draw_routine(self, frame_count: int, ball_count: int):
        self._stdscr.clear()
        # 空のグリッドを作成
        self._grid = [["◯" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE * 2)]

        self._draw_grid(balls[0], 0)
        self._draw_grid(balls[1], 1)

        # １行目のメッセージ
        row0_message = f"frame: {frame_count:> 5} ball: {ball_count:> 3} angle: {angle[0]:> 4}° GRID_SIZE: {GRID_SIZE:< 3}"
        self._stdscr.addstr(0, 0, row0_message)

        # ２行目のメッセージ
        if self._pre_angle != angle[0] or self._count_angle_diff_frame < 1 / FRAMERATE:
            if self._pre_angle != angle[0]:
                self._pre_angle = angle[0]
                self._count_angle_diff_frame = 0
            self._stdscr.addstr(1, 4, "[")
            self._stdscr.addstr("keypress", curses.color_pair(1))
            self._stdscr.addstr(f"] angleを{angle[0]:> 4}° に変更")
            self._count_angle_diff_frame += 1

        # グリッドを描写
        for index, row in enumerate(self._grid):
            row_text = ("  " * GRID_SIZE if index >= GRID_SIZE else "") + " ".join(row)
            self._stdscr.addstr(index + 2, 2, row_text)

        # これは数字を表示するための行
        row_text = ("").join([f"{i:> 2}" for i in range(GRID_SIZE)])[1:]
        self._stdscr.addstr(
            GRID_SIZE * 2 + 2, 0 + 2, f"{row_text} {row_text}", curses.color_pair(1)
        )

        # これは数字を表示するための列
        for index in range(GRID_SIZE * 2):
            self._stdscr.addstr(
                index + 2, GRID_SIZE * 4 + 1, f"{index:> 2}", curses.color_pair(1)
            )

        for index, log in enumerate(self._logs):
            self._stdscr.addstr(
                GRID_SIZE * 2 + 5 + index, 0, "[" + str(index + 1) + "]" + log
            )

            # アラームを表示
        if is_finish_falling[0]:
            self._stdscr.addstr(1, GRID_SIZE * 4 + 4, "Alerm!")

    def _draw_grid(self, balls, index: int):
        # balls配列に基づいてドットを配置
        for ball in balls:
            x, y = ball["x"], ball["y"]
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                self._grid[y + index * GRID_SIZE][x] = "●"

    def print_log(self, message: str):
        """ログを表示する"""
        self._logs.append(message)
