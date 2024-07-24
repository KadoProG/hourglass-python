from animation import animation_routine, fall_ball, remove_ball
import time
from draw import draw_routine
from config import grid_size

# 玉が1マス進む時間（フレームレート）
animation_frame_time = 100 / 1000

# 玉を追加する間隔
interval_between_fall_time = 100 / 1000


# 玉がキャンバスを通過して落下する間隔
interval_between_fall_throuth_time = 1000 / 1000

# ボールの数
ball_length = 60


interval_frequency = interval_between_fall_time / animation_frame_time
interval_canvas_frequency = interval_between_fall_throuth_time / animation_frame_time

canvas_frequency_temp = interval_frequency * ball_length + grid_size


def frame_routine_task_process():
    # フレームを数えるだけ
    frame_count = 0

    # 投げたボールをカウント
    ball_count = 0
    draw_routine(frame_count, ball_count)
    while True:
        animation_routine(0)
        animation_routine(1)
        frame_count = frame_count + 1
        draw_routine(frame_count, ball_count)
        time.sleep(animation_frame_time)
        if frame_count % interval_frequency == 0 and ball_count < ball_length:
            fall_ball()
            ball_count += 1
        if (
            canvas_frequency_temp < frame_count
            and frame_count % interval_canvas_frequency == 0
        ):
            result = remove_ball()
            if result:
                fall_ball(1)


if __name__ == "__main__":
    try:
        frame_routine_task_process()
    except KeyboardInterrupt:
        print("\nプログラムを終了します")
