from config import GRID_SIZE, FRAMERATE, INIT_ANGLE
from animation import balls
import os

grid = [["◯" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
logs = []

# 内部で使用する変数
pre_angle = INIT_ANGLE
_count_angle_diff_frame = 1 / FRAMERATE


def draw_grid(balls, index: int):
    # balls配列に基づいてドットを配置
    for ball in balls:
        x, y = ball["x"], ball["y"]
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            grid[y + index * GRID_SIZE][x] = "●"


def draw_routine(stdscr, frame_count: int, ball_count: int, angle: int, curses):
    global grid, logs, pre_angle, _count_angle_diff_frame

    # 空のグリッドを作成
    grid = [["◯" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE * 2)]

    draw_grid(balls[0], 0)
    draw_grid(balls[1], 1)

    stdscr.clear()

    # １行目のメッセージ
    row0_message = f"frame: {frame_count:> 5} ball: {ball_count:> 3} angle: {angle:> 4}° GRID_SIZE: {GRID_SIZE:< 3}"
    stdscr.addstr(0, 0, row0_message)

    # ２行目のメッセージ
    if pre_angle != angle or _count_angle_diff_frame < 1 / FRAMERATE:
        if pre_angle != angle:
            pre_angle = angle
            _count_angle_diff_frame = 0
        stdscr.addstr(1, 0, "[")
        stdscr.addstr("keypress", curses.color_pair(1))
        stdscr.addstr(f"] angleを{angle:> 4}° に変更")
        _count_angle_diff_frame += 1

    # グリッドを描写
    for index, row in enumerate(grid):
        row_text = ("  " * GRID_SIZE if index >= GRID_SIZE else "") + " ".join(row)
        stdscr.addstr(index + 2, 0, row_text)

    stdscr.addstr(GRID_SIZE * 2 + 3, 0, "[")
    stdscr.addstr("a", curses.color_pair(1))
    stdscr.addstr("]で回転, [")
    stdscr.addstr("q", curses.color_pair(1))
    stdscr.addstr("]または`control + c`で終了")

    for index, log in enumerate(logs):
        stdscr.addstr(GRID_SIZE * 2 + 5 + index, 0, log)

    stdscr.refresh()


def print_log(log: str):
    global logs
    logs.append(log)
