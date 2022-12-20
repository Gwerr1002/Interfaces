from machine import Pin, I2C
#import uasyncio
from time import sleep
import bluetooth
from time import sleep
from ble import BLE_send_sequence
from imu import MPU6050

def config():
    i2c = I2C(1, sda=Pin(23), scl=Pin(22), freq=400000)
    imu = MPU6050(i2c)
    BLE = bluetooth.BLE()
    p = BLE_send_sequence(ble)
    return imu, p

def main():
    imu, p = config()
    while True:
        if p.is_connected():
            ax=imu.accel.x
            ay=imu.accel.y
            az=imu.accel.z
            gx=imu.gyro.x
            gy=imu.gyro.y
            gz=imu.gyro.z
            data = f"{ax} {ay} {az} {gx} {gy} {gz}" + "_"
            p.send(data)
        sleep()

if __name__=="__main__":
    main()