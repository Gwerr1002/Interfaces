from machine import sleep, SoftI2C, Pin,I2C
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM,MAX30105_PULSE_AMP_HIGH
from ssd1306 import *
from utime import ticks_diff, ticks_us
from stacks import Stack_frec

def config():
    # I2C software instance
    i2c = I2C(1,sda=Pin(21),  # Here, use your I2C SDA pin
                  scl=Pin(22),  # Here, use your I2C SCL pin
                  freq=400000)  # Fast: 400kHz, slow: 100kHz
    oled = SSD1306_I2C(128, 64, i2c)
    # Sensor instance
    sensor = MAX30102(i2c=i2c)  # An I2C instance is required

    # Scan I2C bus to ensure that the sensor is connected
    if sensor.i2c_address not in i2c.scan():
        print("Sensor not found.")
        return
    elif not (sensor.check_part_id()):
        # Check that the targeted sensor is compatible
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    # It's possible to set up the sensor at once with the setup_sensor() method.
    # If no parameters are supplied, the default config is loaded:
    # Led mode: 2 (RED + IR)
    # ADC range: 16384
    # Sample rate: 400 Hz
    # Led power: maximum (50.0mA - Presence detection of ~12 inch)
    # Averaged samples: 8
    # pulse width: 411
    print("Setting up sensor with default configuration.", '\n')
    sensor.setup_sensor()

    # It is also possible to tune the configuration parameters one by one.
    # Set the sample rate to 400: 400 samples/s are collected by the sensor
    sensor.set_sample_rate(400)
    # Set the number of samples to be averaged per each reading
    sensor.set_fifo_average(8)
    # Set LED brightness to a medium value
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

    sleep(1)

    # The readTemperature() method allows to extract the die temperature in °C
    print("Reading temperature in °C.", '\n')
    print(sensor.read_temperature())

    # Select whether to compute the acquisition frequency or not
    compute_frequency = False

    print("Starting data acquisition from RED & IR registers...", '\n')
    sleep(1)

    return sensor ,oled, i2c

def main():

    compute_frequency = False
    t_start = ticks_us()  # Starting time of the acquisition
    samples_n = 0  # Number of samples that have been collected

    sensor,oled,i2c = config()
    s = Stack_frec()
    lpm = 0
    aux = 0
    m = 54/2000
    minimo = 17000
    while True:
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
        sensor.check()
        oled.fill_rect(0,0,128,15,0)
        oled.text(f"lpm:{int(lpm)}",0,0)

        # Check if the storage contains available samples
        if sensor.available():
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            #ir_reading = sensor.pop_ir_from_storage()
            print(red_reading)
            aux = s.evaluate_sample(red_reading)
            # Print the acquired data (so that it can be plotted with a Serial Plotter)
            #red_reading = 53*(red_reading-17000)/2000+20
            red_reading = m*(red_reading - minimo) + 30
            #print(red_reading)
            #
            red_reading = int(red_reading)
            if lpm != aux:
                lpm = aux
                oled.pixel(127,63,1)
                #print(s.max,s.min)
                #print(lpm)
                minimo = s.min
                m = 50/(4*(s.max-s.min))
            for i in range(3):
                oled.pixel(127,red_reading-i,1)
            oled.show()
            oled.scroll(-1,0)
            oled.pixel(127,63,0)
            for i in range(3):
                oled.pixel(127,red_reading-i,0)

            if compute_frequency:
                if ticks_diff(ticks_us(), t_start) >= 999999:
                    f_HZ = samples_n
                    samples_n = 0
                    print("acquisition frequency = ", f_HZ)
                    t_start = ticks_us()
                else:
                    samples_n = samples_n + 1


if __name__ == '__main__':
    main()
