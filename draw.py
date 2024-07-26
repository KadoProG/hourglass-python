from config import grid_size
from animation import balls
import os
import time


grid = [["◯" for _ in range(grid_size)] for _ in range(grid_size)]
logs = []

pre_angle = 45
count_angle_diff_frame = 0


def clear_terminal():
    # Windows
    if os.name == "nt":
        os.system("cls")
    # Mac and Linux
    else:
        os.system("clear")


def draw_grid(balls, index: int):
    # balls配列に基づいてドットを配置
    for ball in balls:
        x, y = ball["x"], ball["y"]
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y + index * grid_size][x] = "●"


def draw_routine(stdscr, frame_count: int, ball_count: int, angle: int, curses):
    global grid, logs, pre_angle, count_angle_diff_frame

    # 空のグリッドを作成
    grid = [["◯" for _ in range(grid_size)] for _ in range(grid_size * 2)]

    draw_grid(balls[0], 0)
    draw_grid(balls[1], 1)

    stdscr.clear()

    # １行目のメッセージ
    row0_message = f"frame: {frame_count:< 5} ball: {ball_count:<3} angle: {angle:< 4} grid_size: {grid_size:< 3}"
    stdscr.addstr(0, 0, row0_message)

    # ２行目のメッセージ
    if pre_angle != angle or count_angle_diff_frame < 5:
        if pre_angle != angle:
            pre_angle = angle
            count_angle_diff_frame = 0
        stdscr.addstr(1, 0, f"angleを{angle:< 4}°に変更")
        count_angle_diff_frame += 1

    # グリッドを描写
    for index, row in enumerate(grid):
        row_text = ("  " * grid_size if index >= grid_size else "") + " ".join(row)
        stdscr.addstr(index + 2, 0, row_text)

    stdscr.addstr(grid_size * 2 + 3, 0, "[")
    stdscr.addstr("a", curses.color_pair(1))
    stdscr.addstr("]で回転, [")
    stdscr.addstr("q", curses.color_pair(1))
    stdscr.addstr("]または`control + c`で終了")

    for index, log in enumerate(logs):
        stdscr.addstr(grid_size * 2 + 5 + index, 0, log)

    stdscr.refresh()


def print_log(log: str):
    global logs
    logs.append(log)
