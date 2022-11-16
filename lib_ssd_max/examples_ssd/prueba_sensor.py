from max30102 import MAX30102
from machine import Pin, I2C

my_SDA_pin = 21  # I2C SDA pin number here!
my_SCL_pin = 22  # I2C SCL pin number here!
my_i2c_freq = 400000  # I2C frequency (Hz) here!

i2c = I2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin),
              freq=my_i2c_freq)

sensor = MAX30102(i2c=i2c)

# Setup with default values
#sensor.setup_sensor()

# Alternative example:
sensor.setup_sensor(led_mode=2, adc_range=16384, sample_rate=400)

# Set the number of samples to be averaged by the chip
SAMPLE_AVG = 8  # Options: 1, 2, 4, 8, 16, 32
sensor.set_fifo_average(SAMPLE_AVG)

# Set the ADC range
ADC_RANGE = 4096  # Options: 2048, 4096, 8192, 16384
sensor.set_adc_range(ADC_RANGE)

# Set the sample rate
SAMPLE_RATE = 400  # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
sensor.set_sample_rate(SAMPLE_RATE)

# Set the Pulse Width
PULSE_WIDTH = 118  # Options: 69, 118, 215, 411
sensor.set_pulse_width(PULSE_WIDTH)

# Set the LED mode
LED_MODE = 2  # Options: 1 (red), 2 (red + IR), 3 (red + IR + g - MAX30105 only)
sensor.set_led_mode(LED_MODE)

# Set the LED brightness of each LED

# Options:
# MAX30105_PULSE_AMP_LOWEST =  0x02 # 0.4mA  - Presence detection of ~4 inch
# MAX30105_PULSE_AMP_LOW =     0x1F # 6.4mA  - Presence detection of ~8 inch
MAX30105_PULSEAMP_MEDIUM =  0x7F # 25.4mA - Presence detection of ~8 inch
# MAX30105_PULSE_AMP_HIGH =    0xFF # 50.0mA - Presence detection of ~12 inch
LED_POWER = MAX30105_PULSEAMP_MEDIUM
sensor.set_pulse_amplitude_red(LED_POWER)
sensor.set_pulse_amplitude_it(LED_POWER)
sensor.set_pulse_amplitude_green(LED_POWER)

# Set the LED brightness of all the active LEDs
LED_POWER = MAX30105_PULSEAMP_MEDIUM
# Options:
# MAX30105_PULSE_AMP_LOWEST =  0x02 # 0.4mA  - Presence detection of ~4 inch
# MAX30105_PULSE_AMP_LOW =     0x1F # 6.4mA  - Presence detection of ~8 inch
# MAX30105_PULSE_AMP_MEDIUM =  0x7F # 25.4mA - Presence detection of ~8 inch
# MAX30105_PULSE_AMP_HIGH =    0xFF # 50.0mA - Presence detection of ~12 inch
sensor.set_active_leds_amplitude(LED_POWER)

while (True):
    # The check() method has to be continuously polled, to check if
    # there are new readings into the sensor's FIFO queue. When new
    # readings are available, this function will put them into the storage.
    sensor.check()

    # Check if the storage contains available samples
    if (sensor.available()):
        # Access the storage FIFO and gather the readings (integers)
        red_sample = sensor.pop_red_from_storage()
        ir_sample = sensor.pop_ir_from_storage()

        # Print the acquired data (can be plot with Arduino Serial Plotter)
        print(red_sample, ",", ir_sample)

