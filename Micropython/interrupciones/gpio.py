from machine import Pin, mem32

LED = 22
BTN = 23
MAP_LED = (1<<LED)
MAP_BTN = (1<<BTN)

GPIO_OUT_REG1 = 0x3FF44004

def on_off(pin):
    mem32[GPIO_OUT_REG1] ^= MAP_LED

def conf():
    led = Pin(LED,mode = Pin.OUT)
    led.off()
    btn = Pin(BTN,mode = Pin.IN)
    btn.irq(trigger=Pin.IRQ_RISING+Pin.IRQ_FALLING, handler = on_off)
    
if __name__ == '__main__':
    conf()
    while True:
        pass
