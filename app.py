import curses
from run import frame_routine_task_process
from flask import Flask
import argparse
import threading
from src.draw import Draw
from src.events.input_changes import input_thread
from src.sand_animation import SandAnimation
import os
from dotenv import load_dotenv

load_dotenv()
boot = os.getenv("BOOT")
app = Flask(__name__)

def main(stdscr: curses.window):
    @app.route("/")
    def hello_world():
        return "Hello World"


    @app.route("/start")
    def start():
        sandAnimation.start_stop_click()
        return "start"
      
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", help="optional", action="store_true")
    args = parser.parse_args()

    is_fixed = args.fix

    # 停止イベントを作成
    stop_event = threading.Event()

    # 描画クラスを作成
    draw = Draw(stdscr, is_fixed)
    sound = None

    if boot == "raspberrypi":
        from src.sound.bibideba import Bibideba

        sound = Bibideba()
    elif boot == "macos":
        from src.sound.sound import Sound

        sound = Sound()

    else:
        from src.sound.sound_mock import SoundMock

        sound = SoundMock()

    sandAnimation = SandAnimation(sound, is_fixed)

    if boot == "raspberrypi":
        from src.events.button import button_thread

        button_thread_obj = threading.Thread(
            target=button_thread,
            args=(stop_event, sandAnimation.start_stop_click),
            daemon=True,
        )
        # 入力スレッドを開始
        button_thread_obj.start()

    input_thread_obj = threading.Thread(
        target=input_thread, args=(stop_event, stdscr, draw, sandAnimation), daemon=True
    )

    # 入力スレッドを開始
    input_thread_obj.start()

    # メイン処理を実行
    frame_routine_task_process(draw, sandAnimation, is_fixed)

 

def wrapper_main():
    curses.wrapper(main)

# アプリケーションを実行
if __name__ == '__main__':
        # Flaskアプリケーションをスレッドで実行
    flask_thread = threading.Thread(target=app.run)
    
    # cursesをスレッドで実行
    curses_thread = threading.Thread(target=wrapper_main)
    
    # スレッドを開始
    flask_thread.start()
    curses_thread.start()
    
    # スレッドが終了するのを待機
    flask_thread.join()
    curses_thread.join()
