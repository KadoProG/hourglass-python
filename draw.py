from config import grid_size
from animation import balls
import os
import time


grid = [["◯" for _ in range(grid_size)] for _ in range(grid_size)]
logs = []


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


def draw_routine(frame_count: int, ball_count: int):
    global grid, logs

    # 空のグリッドを作成
    grid = [["◯" for _ in range(grid_size)] for _ in range(grid_size * 2)]

    draw_grid(balls[0], 0)
    draw_grid(balls[1], 1)

    clear_terminal()

    # グリッドを描写（in terminal）
    for index, row in enumerate(grid):
        print(("  " * grid_size if index >= grid_size else "") + " ".join(row))
    print()
    print(f"frame: {frame_count} ball: {ball_count}")
    for log in logs:
        print(log)


def print_log(log: str):
    global logs
    logs.append(log)
