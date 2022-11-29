from obj_ox  import (config, Pin,
                     adq_signal, update_oled,
                     uasyncio, temperatura)
#
def main():
    pin_bpm = Pin(26, Pin.OUT) #Salida para activar el buzzer activo
    sensor, oled, i2c = config() #Configuración del sensor y OLED
    loop = uasyncio.get_event_loop() #Crear bucle
    #Tarea para adquirir señal, medir frecuencia cardiaca y mostrar datos en OLED
    loop.create_task(adq_signal(sensor,oled,pin_bpm))
    #Tarea para adquirir temperatura
    loop.create_task(temperatura(sensor))
    loop.run_forever()
#
if __name__ == '__main__':
    main()
