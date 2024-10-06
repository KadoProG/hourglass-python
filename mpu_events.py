# VCC - 3.3V pin1
# GND - GND pin6, 9, 14, 20, 25, 30, 34, 39
# SCL - GPIO3 (SCL) pin5
# SDA - GPIO2 (SDA) pin3

import smbus
import time
import math

# MPU9250のI2Cアドレス
MPU9250_ADDRESS = 0x68

# レジスタアドレス
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

# I2Cバスの初期化
bus = smbus.SMBus(1)


def _read_word(sensor_address, reg_address):
    high = bus.read_byte_data(sensor_address, reg_address)
    low = bus.read_byte_data(sensor_address, reg_address + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value


def _read_accel_data():
    accel_x = _read_word(MPU9250_ADDRESS, ACCEL_XOUT_H)
    accel_y = _read_word(MPU9250_ADDRESS, ACCEL_YOUT_H)
    accel_z = _read_word(MPU9250_ADDRESS, ACCEL_ZOUT_H)
    return accel_x, accel_y, accel_z


# 傾きの計算
def _calculate_tilt(accel_x, accel_y, accel_z):
    roll = math.atan2(accel_y, accel_z) * 180 / math.pi
    pitch = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi
    return round(roll), round(pitch)


def get_mpu_angle():
    """
    角度を求める関数
    """
    accel_x, accel_y, accel_z = _read_accel_data()
    return _calculate_tilt(accel_x, accel_y, accel_z)


def main():
    while True:
        try:
            roll, pitch = get_mpu_angle()
            print(f"Roll: {roll:.2f}, Pitch: {pitch:.2f}")
        except Exception as e:
            print(f"Error reading data: {e}")
        time.sleep(0.1)


# スクリプトとして実行された場合
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("プログラムが正常に終了されました")
