from machine import sleep, Pin, I2C
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM,MAX30105_PULSE_AMP_HIGH
from ssd1306 import *
from stacks import Stack_frec
import uasyncio
from _thread import start_new_thread

T = 0 #Dato de la temperatura
ans = 0 #Dato de muestra anterior para referencia del OLED

#Configuracion del oled y sensor
def config():
    i2c = I2C(1,sda=Pin(21), scl=Pin(22), freq=400000) #Instancia I2C por hardware
    oled = SSD1306_I2C(128, 64, i2c) #instancia del oled
    oled.contrast(1)#el menor contraste
    sensor = MAX30102(i2c=i2c)  #instancia del sensor
    #
    # Escanear el bus I2C para asegurarse que el sensor esta conectado.
    if sensor.i2c_address not in i2c.scan():
        print("Sensor no encontrado.")
        return
    elif not (sensor.check_part_id()):
        # Verificar que el sensor sea compatible
        print("Dispositivo I2C ID no esta respondiendo, correspondiente a MAX30102")
        return
    else:
        print("Sensor reconocido; status: conectado")
    sensor.setup_sensor()#Configurar sensor con valores por default
    sensor.set_sample_rate(3200) #3200 muestras/segundo
    sensor.set_fifo_average(16) #numero de muestras a ser promediadas por cada lectura
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM) # configurar el brillo del LED al valor medio
    #
    sleep(1)
    print("Comenzando adquisicion de datos, temperatura y frecuencia cardiaca", '\n')
    sleep(1)
    #
    return sensor, oled, i2c

#Funcion para mostrar datos en el OLED
def update_oled(oled,red_reading,lpm):
    global T, ans
    oled.fill_rect(0,0,128,15,0) #Borra una sección rectangular del OLED
    oled.text(f"lpm:{int(lpm)}",0,0) #Escribe frecuencia cardiaca
    oled.text(f"T:{int(T)}",63,0) #Escribe temperatura
    '''
    Muestra el dato actual en pantalla con un ancho de linea de 3 pixeles
    también se detecta si hay una pendiente positiva y negativa entre el valor
    anterior y el actual para interpolar pixeles y no se vean muchos saltos en
    el OLED
    '''
    if ans-red_reading > 0:
        signo = 1
    else:
        signo = -1
    for i in range(2):
        for j in range(3):
            oled.vline(125+j,red_reading+i*signo,3,1)
    oled.show()#Muestra los datos en pantalla
    oled.scroll(-3,0)#Recorre la información del OLED tres pixeles a la izquierda
    #Las siguientes lineas borran los datos anteriores en el oled para no acarrearlos
    for i in range(2):
        for j in range(3):
            oled.vline(125+j,red_reading+i*signo,3,0)
    ans = red_reading

async def adq_signal(sensor,oled,lec_adqfreq):
    lpm = 0 #para guardar la frecuencia cardiaca
    aux = 0 #detección de un cambio en la frecuencia cardiaca para actualizar
    #Se hizo una regresión de la forma y-30 = m*(x-minimo)
    m = 54/2000 #pendiente de la regresión
    minimo = 17000 #valor para la regresión
    s = Stack_frec() #pila para la detección de máximos, minimos y deteccion de la frecuencia
    while True:
        sensor.check() #verificar si hay nuevas lecturas en la pila FIFO del sensor
        #
        if sensor.available(): # Ver si el sensor tiene muestras disponibles
            red_reading = sensor.pop_red_from_storage() #Acceder a la pila FIFO del sensor y leer la información
            #print(red_reading) #leer la adquisición en consola
            aux = s.evaluate_sample(red_reading) #evaluar muestra en la pila para max, min. Regresa valor actual lpm
            red_reading = m*(red_reading - minimo) + 30 #regresión lineal para mostrar en OLED
            red_reading = int(red_reading) #Conversion a entero para mostrar en OLED
            lec_adqfreq.off() #apagar el pin del buzzer
            #Actualizar frecuencia cardiaca
            if lpm != aux:
                lpm = aux #Actualizar frecuencia cardiaca
                lec_adqfreq.on() #Encender el aviso de detección de pico (buzzer)
                minimo = s.min #Actualizar minimo
                amplitud = s.max-s.min
                if amplitud > 0:
                    m = 50/(4*(amplitud)) #actualizar pendiente de la regresión
            update_oled(oled,red_reading,lpm) #para mostrar gráfica en OLED
            await uasyncio.sleep_ms(1) #esperar 1 ms
#Leer temperatura cada 5 segundos
async def temperatura(sensor):
    global T
    while True:
        T=sensor.read_temperature() #leer temperatura
        await uasyncio.sleep(5) #esperar 5 segundos
