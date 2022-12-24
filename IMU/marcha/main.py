#1
from machine import Pin, I2C, mem32
import uasyncio
from time import sleep_ms
import bluetooth
from ble import BLE_send_sequence
from imu import MPU6050

data = ""
LED = 21

def config():
    global LED
    i2c = I2C(1, sda=Pin(23), scl=Pin(22), freq=400000)
    imu = MPU6050(i2c)
    led = Pin(LED,Pin.OUT)
    BLE = bluetooth.BLE()
    p = BLE_send_sequence(BLE)
    return imu, p

async def adq(imu,p):
    global data, LED
    GPIO_OUT_REG = 0x3FF44004
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
            mem32[GPIO_OUT_REG]^= (1<<LED)
        await uasyncio.sleep_ms(17)

async def ble_send(p):
    global data
    while True:
        if p.is_connected():
            #print(f"sending: {data}")
            p.send(data)
            #print("sended")
            data = ""
        await uasyncio.sleep_ms(90)


def main():
    imu, p = config()
    loop = uasyncio.get_event_loop()
    loop.create_task(adq(imu,p))
    loop.create_task(ble_send(p))
    #
    loop.run_forever()

if __name__=="__main__":
    main()