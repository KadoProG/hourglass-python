# micropythonでbibidebaを演奏するプログラム
# machineモジュールを使っているため、Raspberry Pi Picoでのみ動作します
from machine import Pin, PWM
from time import sleep

# 設定
BUZZER_PIN = 27  # GPIO 27

# GPIOの設定
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty_u16(32768)  # デューティサイクルを50%に設定（16ビット精度）


def play_sound(tone: int, duration: float):
    buzzer.freq(tone)
    sleep(duration)


#    buzzer.duty_u16(0)  # デューティサイクルを0にして停止
#    sleep(0.05)  # 短いポーズを追加

# ここから音程を刻み込む
buzzer.duty_u16(32768)  # デューティサイクルを50%に設定（16ビット精度）


def play_bibideba_chorus_common():
    play_sound(430, 0.127)  # BI
    play_sound(480, 0.127)  # BBI
    play_sound(430, 0.254)  # DI
    play_sound(430, 0.127)  # BO
    play_sound(480, 0.127)  # BBI
    play_sound(430, 0.254)  # DI
    play_sound(480, 0.381)  # BOO
    play_sound(320, 0.381)  # WA
    play_sound(430, 0.127)  # BI
    play_sound(480, 0.127)  # BBI
    play_sound(430, 0.127)  # DI
    play_sound(480, 0.127)  # BO
    play_sound(430, 0.127)  # BBI
    play_sound(430, 0.127)  # DI
    play_sound(480, 0.254)  # BOO
    play_sound(320, 0.508)  # BA
    play_sound(462, 0.254)  # YEAH
    play_sound(430, 0.254)  #
    play_sound(382, 0.254)  #


def play_song():
    play_bibideba_chorus_common()  # 繰り返し部分

    play_sound(320, 0.254)  # 混（こん）
    play_sound(382, 0.127)  # 絡（が）
    play_sound(430, 0.127)  # （ら）
    play_sound(480, 0.254)  # がっ
    play_sound(320, 0.127)  # て
    play_sound(285, 0.127)  # も
    play_sound(320, 0.254)  # 仕様（しよう）
    play_sound(480, 0.127)  # が
    play_sound(462, 0.127)  #
    play_sound(480, 0.381)  # ない
    play_sound(320, 0.127)  # ガ
    play_sound(382, 0.127)  # ラ
    play_sound(430, 0.127)  # ス
    play_sound(480, 0.254)  # シュー
    play_sound(320, 0.127)  # ズ
    play_sound(285, 0.127)  # で
    play_sound(320, 0.254)  # お
    play_sound(480, 0.127)  # とっ
    play_sound(462, 0.127)  #
    play_sound(480, 0.508)  # ない

    play_bibideba_chorus_common()  # 繰り返し部分

    play_sound(320, 0.254)  # こん
    play_sound(382, 0.127)  # や
    play_sound(430, 0.127)  # に
    play_sound(480, 0.254)  # あす
    play_sound(320, 0.127)  # な
    play_sound(285, 0.127)  # ど
    play_sound(320, 0.254)  # な
    play_sound(620, 0.127)  # ーい
    play_sound(660, 0.254)  # ーい
    play_sound(462, 0.127)  # な
    play_sound(430, 0.127)  # ら
    play_sound(382, 0.127)  # ば
    play_sound(430, 0.254)  # 自由
    play_sound(382, 0.127)  # に
    play_sound(430, 0.254)  # 踊っ
    play_sound(382, 0.127)  # た
    play_sound(430, 0.127)  # も
    play_sound(382, 0.127)  # ん
    play_sound(430, 0.127)  # が
    play_sound(480, 0.381)  # ち
    play_sound(285, 0.127)  # で
    play_sound(320, 0.381)  # しょ


def main():
    try:
        play_song()
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
    finally:
        buzzer.deinit()  # PWMを終了


if __name__ == "__main__":
    main()
