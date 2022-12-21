from machine import Pin, I2C
import uasyncio
from time import sleep_ms
import bluetooth
from ble import BLE_send_sequence
from imu import MPU6050

data = ""

def config():
    i2c = I2C(1, sda=Pin(23), scl=Pin(22), freq=400000)
    imu = MPU6050(i2c)
    BLE = bluetooth.BLE()
    p = BLE_send_sequence(BLE)
    return imu, p

async def adq(imu,p):
    global data
    while True:
        if p.is_connected():
            ax=imu.accel.x
            ay=imu.accel.y
            az=imu.accel.z
            gx=imu.gyro.x
            gy=imu.gyro.y
            gz=imu.gyro.z
            data += f"{ax} {ay} {az} {gx} {gy} {gz}" + ","
            #print(data)
        await uasyncio.sleep_ms(17)

async def ble_send(p):
    global data
    while True:
        if p.is_connected():
            print(f"sending: {data}")
            p.send(data)
            print("sended")
            data = ""
        await uasyncio.sleep_ms(100)


def main():
    global data
    imu, p = config()
    loop = uasyncio.get_event_loop()
    loop.create_task(adq(imu,p))
    loop.create_task(ble_send(p))
    #
    loop.run_forever()

if __name__=="__main__":
    main()