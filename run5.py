import curses
import threading
import argparse
import os
from dotenv import load_dotenv
from run import frame_routine_task_process
from app.draw import Draw
from app.events.input_changes import input_thread
from app.sand_animation import SandAnimation
from app.sound import sound
import curses
import socketio
import threading



# 環境変数の読み込み
load_dotenv()
boot = os.getenv("BOOT")
sensor = os.getenv("SENSOR")
socketio_url = os.getenv("SOCKETIO_URL")


# グローバルで sandAnimation を定義
sandAnimation = None


# Socket.IO クライアントを作成
sio = socketio.Client()


# サーバーに接続されたときのイベントハンドラ
@sio.event
def connect():
    print("Connected to server")


# サーバーからメッセージを受け取ったときのイベントハンドラ
@sio.event
def message(data):
    try:
        if data['type'] == "control":
            print('Received control message:', data['control'])
            if data['control'] == "start":
                sandAnimation.start_stop_click()
            elif data['control'] == "angle":
                sandAnimation.set_angle()
            else:
                print("Unknown control message:", data)
            
    except:
        print("Received message:", data)


# サーバーとの接続が切断されたときのイベントハンドラ
@sio.event
def disconnect():
    print("Disconnected from server")


# サーバーに接続
params = {"device": "raspberrypi", "nickname": "Python Client"}
sio.connect(socketio_url, auth=params)

# サーバーにメッセージを送信
sio.send("Hello from Python client!")




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
    sandAnimation = SandAnimation(sound(), is_fixed, sio)

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


def main():
    """
    メインのエントリーポイント
    """
    # 引数をパース
    is_fixed = initialize_parser()

    # サーバーからのメッセージを待ち受けるスレッドを開始
    wait_thread = threading.Thread(target=sio.wait)

    # cursesを別スレッドで実行
    curses_thread = threading.Thread(target=wrapper_main, args=(is_fixed,))

    # スレッドを開始
    curses_thread.start()
    # time.sleep(1)
    wait_thread.start()

    # スレッドが終了するのを待機
    wait_thread.join()
    curses_thread.join()


# アプリケーションを実行
if __name__ == "__main__":
    main()
