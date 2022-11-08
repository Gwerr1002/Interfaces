#sudo ampy --port /dev/ttyUSB0 run blink.py
from machine import Pin, mem32
from time import sleep
led=Pin(26,Pin.OUT)
x^=1
while True:
    led.value(x)
    x^=1
    sleep(1)


GPIO_OUT_REG = 0x3FF44004
PIN0=26
PIN1=27
LED0=Pin(PIN0, Pin.OUT)
LED1=Pin(PIN1,Pin.OUT)
while True:
    mem32[GPIO_OUT_REG] ^= (1<<PIN0) | (1<<PIN1)#RECORREMOS 26 BITS Y 27 BITS
    sleep(0.5)
