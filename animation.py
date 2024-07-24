from typing import Optional
from config import grid_size

is_positive_sine = True
is_positive_cosine = True

balls = [[], []]


def animation_routine(canvasIndex):
    global is_positive_sine, is_positive_cosine, balls
    for index, ball in enumerate(balls[canvasIndex]):
        x = ball["x"] + (1 if is_positive_sine else -1)
        y = ball["y"] + (1 if is_positive_cosine else -1)

        isRightEnd = False
        isBottomEnd = False

        isBottomRightEmpty = True
        isBottomEmpty = True
        isBottomLeftEmpty = True

        if is_positive_sine and x == grid_size:
            x -= 1
            isRightEnd = True
        elif not is_positive_sine and x == -1:
            x += 1
            isRightEnd = True

        if is_positive_cosine and y == grid_size:
            y -= 1
            isBottomEnd = True
        elif not is_positive_cosine and y == -1:
            y += 1
            isBottomEnd = True

        if isRightEnd and isBottomEnd:
            ball["x"] = x
            ball["y"] = y
            continue

        for index2, b in enumerate(balls[canvasIndex]):
            if index == index2:
                continue
            if b["x"] == x and b["y"] == y:
                isBottomEmpty = False
            if b["x"] == x and b["y"] == (y - 1 if is_positive_cosine else y + 1):
                isBottomRightEmpty = False
            if b["x"] == (x - 1 if is_positive_sine else x + 1) and b["y"] == y:
                isBottomLeftEmpty = False

        if not isBottomEmpty:
            if isBottomRightEmpty:
                y -= 1 if is_positive_cosine else y + 1
            elif isBottomLeftEmpty:
                x -= 1 if is_positive_sine else x + 1
            else:
                y -= 1 if is_positive_cosine else y + 1
                x -= 1 if is_positive_sine else x + 1

        ball["x"] = x
        ball["y"] = y


def fall_ball(type: Optional[int] = None):
    global balls
    x = 0 if is_positive_sine else grid_size - 1
    y = 0 if is_positive_cosine else grid_size - 1

    canvas_index = 0

    if type is None:
        pass
    else:
        canvas_index = 1 if is_positive_sine else 0

    balls[canvas_index].append({"x": x, "y": y})
    return f"{len(balls[0])}, {len(balls[1])}"


def remove_ball():
    global is_positive_sine, is_positive_cosine, balls
    x = grid_size - 1 if is_positive_sine else 0
    y = grid_size - 1 if is_positive_cosine else 0

    canvas_index = 0 if is_positive_sine else 1

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
