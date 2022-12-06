from machine import Timer, mem32, Pin

PIN_LED_7 = 22
PIN_LED_11 = 23
MAP_LED_7HZ = (1<<PIN_LED_7)
MAP_LED_11HZ = (1<<PIN_LED_11)


GPIO_OUT_REG1 = 0x3FF44004

def toggle_7hz(timer):
    mem32[GPIO_OUT_REG1] ^= MAP_LED_7HZ

def toogle_11hz(timer):
    mem32[GPIO_OUT_REG1] ^= MAP_LED_11HZ

def config():
    led7 = Pin(PIN_LED_7, mode = Pin.OUT)
    led11= Pin(PIN_LED_11,mode = Pin.OUT)
    led7.value(1)
    led11.value(1)
    timer7 = Timer(0)
    timer7.init(period = 71, mode = Timer.PERIODIC, callback= toggle_7hz)
    timer11 = Timer(1)
    timer11.init(period= 45, mode = Timer.PERIODIC,callback = toogle_11hz)

config()
while True:
    pass
