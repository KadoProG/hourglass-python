import math
from typing import Optional
from config import grid_size, angle

is_positive_sine = True
is_positive_cosine = True

balls = [[], []]


def animation_routine():
    global is_positive_sine, is_positive_cosine, balls
    for canvas_index in range(len(balls)):
        for index, ball in enumerate(balls[canvas_index]):
            x = ball["x"] + (1 if is_positive_sine else -1)
            y = ball["y"] + (1 if is_positive_cosine else -1)

            is_right_end = False
            is_bottom_end = False

            is_bottom_right_empty = True
            is_bottom_empty = True
            is_bottom_left_empty = True

            # x軸に対して、はみ出し確認と位置調整
            if is_positive_sine and x == grid_size:
                x -= 1
                is_right_end = True
            elif not is_positive_sine and x == -1:
                x += 1
                is_right_end = True

            # y軸に対して、はみ出し確認と位置調整
            if is_positive_cosine and y == grid_size:
                y -= 1
                is_bottom_end = True
            elif (not is_positive_cosine) and y == -1:
                y += 1
                is_bottom_end = True

            # x軸とy軸の両方該当する場合、保存しアニメーション処理を終了
            if is_right_end and is_bottom_end:
                ball["x"] = x
                ball["y"] = y
                continue

            # 他のボールとの衝突判定
            for index2, b in enumerate(balls[canvas_index]):
                if index == index2:
                    continue
                if b["x"] == x and b["y"] == y:
                    is_bottom_empty = False
                if b["x"] == x and b["y"] == (y - 1 if is_positive_cosine else y + 1):
                    is_bottom_right_empty = False
                if b["x"] == (x - 1 if is_positive_sine else x + 1) and b["y"] == y:
                    is_bottom_left_empty = False

            if not is_bottom_empty:
                if is_bottom_right_empty:
                    y = y - 1 if is_positive_cosine else y + 1
                elif is_bottom_left_empty:
                    x = x - 1 if is_positive_sine else x + 1
                else:
                    y = y - 1 if is_positive_cosine else y + 1
                    x = x - 1 if is_positive_sine else x + 1

            ball["x"] = x
            ball["y"] = y


# ボールを落とす
# type: None以外の場合、指定したキャンバスにボールを落とす
def fall_ball(canvas_index: int):
    global is_positive_sine, is_positive_cosine, balls
    x = 0 if is_positive_sine else grid_size - 1
    y = 0 if is_positive_cosine else grid_size - 1

    balls[canvas_index].append({"x": x, "y": y})


def remove_ball(canvas_index: Optional[int] = None):
    global is_positive_sine, is_positive_cosine, balls

    x = grid_size - 1 if is_positive_sine else 0
    y = grid_size - 1 if is_positive_cosine else 0

    if canvas_index is None:
        for i in range(len(balls)):
            index = find_index(balls[i], lambda ball: ball["x"] == x and ball["y"] == y)
            if index == -1:
                continue
            else:
                del balls[i][index]
                return True
        return False
    else:
        index = find_index(
            balls[canvas_index], lambda ball: ball["x"] == x and ball["y"] == y
        )
        if index == -1:
            return False
        else:
            del balls[canvas_index][index]
            return True


def find_index(lst, predicate):
    for i, x in enumerate(lst):
        if predicate(x):
            return i
    return -1


def update_angle():
    global is_positive_sine, is_positive_cosine
    angle[0] += 90
    if angle[0] > 180:
        angle[0] -= 360
    angle[0] = angle[0]
    is_positive_sine = math.sin((angle[0] * math.pi) / 180) >= 0
    is_positive_cosine = math.cos((angle[0] * math.pi) / 180) >= 0

    return f"{is_positive_sine}, {is_positive_cosine}"


def fall_ball_throuth_canavs():
    global is_positive_sine, is_positive_cosine
    if math.tan((angle[0] * math.pi) / 180) <= 0:
        return
    result = remove_ball(0 if is_positive_sine else 1)
    if result:
        fall_ball(1 if is_positive_sine else 0)
