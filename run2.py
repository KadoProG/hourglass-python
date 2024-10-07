from app.flask_init import create_app
import curses
import threading
import argparse
import os
from dotenv import load_dotenv
from run import frame_routine_task_process
from app.draw import Draw
from app.events.input_changes import input_thread
from app.sand_animation import SandAnimation
import time
from app.sound import sound

# 環境変数の読み込み
load_dotenv()
boot = os.getenv("BOOT")
sensor = os.getenv("SENSOR")


# グローバルで sandAnimation を定義
sandAnimation = None


def initialize_parser():
    """
    コマンドライン引数の解析
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", help="optional", action="store_true")
    args = parser.parse_args()
    return args.fix


def curses_main(stdscr: curses.window, is_fixed: bool):
    """
    cursesのメイン処理
    """
    global sandAnimation  # sandAnimation をグローバルで初期化
    # 停止イベントの作成
    stop_event = threading.Event()

    # 描画クラスとサウンドの初期化
    draw = Draw(stdscr, is_fixed, True)

    # サンドアニメーションの初期化
    sandAnimation = SandAnimation(sound(), is_fixed)

    # raspberrypi環境でのボタンスレッドの初期化
    if boot == "raspberrypi" and sensor == "true":
        from app.events.button import button_thread

        button_thread_obj = threading.Thread(
            target=button_thread,
            args=(stop_event, sandAnimation.start_stop_click),
            daemon=True,
        )
        button_thread_obj.start()

    # 入力スレッドの開始
    input_thread_obj = threading.Thread(
        target=input_thread, args=(stop_event, stdscr, draw, sandAnimation), daemon=True
    )
    input_thread_obj.start()

    # メイン処理の実行
    frame_routine_task_process(draw, sandAnimation, is_fixed)


def wrapper_main(is_fixed: bool):
    """
    cursesラッパーを使ってメイン処理を呼び出す
    """
    curses.wrapper(curses_main, is_fixed)


def run_flask_app():
    """
    Flaskアプリケーションを実行
    """
    app = create_app(sandAnimation)
    app.run(debug=True, use_reloader=False, host="0.0.0.0")


def main():
    """
    メインのエントリーポイント
    """
    # 引数をパース
    is_fixed = initialize_parser()

    # Flaskアプリケーションを別スレッドで実行
    flask_thread = threading.Thread(target=run_flask_app)

    # cursesを別スレッドで実行
    curses_thread = threading.Thread(target=wrapper_main, args=(is_fixed,))

    # スレッドを開始
    curses_thread.start()
    time.sleep(1)
    flask_thread.start()

    # スレッドが終了するのを待機
    flask_thread.join()
    curses_thread.join()


# アプリケーションを実行
if __name__ == "__main__":
    main()
