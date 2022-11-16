from machine import (Pin as PIN, I2C)
from max30102 import *
from ssd1306 import *
from time import sleep

#inicializar el protocolo I2C

i2c = I2C(1, sda = PIN(21), scl = PIN(22))

# Configuración OLED 
oled = SSD1306_I2C(128, 64, i2c)
oled.text("Hola",0,0)
oled.text("Conectando",0,10)
oled.text("sensor :)",0,20)
oled.show()

# Configuracion sensor

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()
SAMPLE_AVG = 8  # Options: 1, 2, 4, 8, 16, 32
sensor.set_fifo_average(SAMPLE_AVG)
ADC_RANGE = 4096  # Options: 2048, 4096, 8192, 16384
sensor.set_adc_range(ADC_RANGE)
SAMPLE_RATE = 400  # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
sensor.set_sample_rate(SAMPLE_RATE)
PULSE_WIDTH = 118  # Options: 69, 118, 215, 411
sensor.set_pulse_width(PULSE_WIDTH)
LED_MODE = 2  # Options: 1 (red), 2 (red + IR), 3 (red + IR + g - MAX30105 only)
sensor.set_led_mode(LED_MODE)
LED_POWER = 0x7F
sensor.set_active_leds_amplitude(LED_POWER)

oled.fill(0)
oled.show()
oled.text("red:",0,0)
oled.text("ir:",0,10)

sleep(1)

while True:
    sleep(1)
    sensor.check()
    # Check if the storage contains available samples
    if (sensor.available()):
        # Access the storage FIFO and gather the readings (integers)
        red_sample = sensor.pop_red_from_storage()
        ir_sample = sensor.pop_ir_from_storage()
        oled.fill_rect(40, 0, 64, 64, 0)
        oled.show()
        oled.text(f"{red_sample}",40,0)
        oled.text(f"{ir_sample}",40,10)
        oled.show()
        
        