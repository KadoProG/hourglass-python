import math
from typing import Optional
from config import GRID_SIZE, angle, balls, is_finish_falling

is_positive_sine = True
is_positive_cosine = True


def animation_routine():
    """ボールの１フレームごとの動きを変数内で描写する関数"""
    global is_positive_sine, is_positive_cosine
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
            if is_positive_sine and x == GRID_SIZE:
                x -= 1
                is_right_end = True
            elif not is_positive_sine and x == -1:
                x += 1
                is_right_end = True

            # y軸に対して、はみ出し確認と位置調整
            if is_positive_cosine and y == GRID_SIZE:
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


def fall_ball(canvas_index: int):
    """
    ボールを落とす関数

    canvas_indexによってどちらのキャンバスに落とすかを指定
    """
    global is_positive_sine, is_positive_cosine
    x = 0 if is_positive_sine else GRID_SIZE - 1
    y = 0 if is_positive_cosine else GRID_SIZE - 1

    balls[canvas_index].append({"x": x, "y": y})


def remove_ball(canvas_index: Optional[int] = None):
    """
    ボールを削除する関数\n
    `canvas_index`によってどちらのキャンバスのボールを削除するかを指定\n
    `canvas_index`が`None`の場合、どちらかのボールを削除する\n
    削除が成功したかを`boolean`を返す
    """
    global is_positive_sine, is_positive_cosine

    x = GRID_SIZE - 1 if is_positive_sine else 0
    y = GRID_SIZE - 1 if is_positive_cosine else 0

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
    """
    角度を更新する関数\n
    45→135→-135→-45→45の順に更新する\n
    角度を更新するとともに、`is_positive_sine`と`is_positive_cosine`を更新する
    """
    global is_positive_sine, is_positive_cosine
    is_finish_falling[0] = False
    angle[0] += 90
    if angle[0] > 180:
        angle[0] -= 360
    angle[0] = angle[0]
    is_positive_sine = math.sin((angle[0] * math.pi) / 180) >= 0
    is_positive_cosine = math.cos((angle[0] * math.pi) / 180) >= 0

def fall_ball_throuth_canavs():
    """
    ボールをキャンバスを通して落下させる関数\n
    上側のボールの削除と、下側のボールの落下を行い、砂の落下をシミュレートする\n
    砂が落下し終えた場合、`is_finish_falling`を`True`にする
    """
    global is_positive_sine, is_positive_cosine
    if math.tan((angle[0] * math.pi) / 180) <= 0:
        is_finish_falling[0] = False
        return
    result = remove_ball(0 if is_positive_sine else 1)
    if result:
        fall_ball(1 if is_positive_sine else 0)

    # 砂が落下し終えた場合の処理
    if len(balls[0 if is_positive_sine else 1]) == 0:
        is_finish_falling[0] = True
    else:
        is_finish_falling[0] = False
