import machine as mn
import network
import urequests
import time

import gc
gc.collect()

#https://ifttt.com/ activar un webhook
#https://ifttt.com/my_services --> consultar los servicios que tienen activos --> 
#                              --> ir a la documentación del webhook y copiar al api-key
#lanzar el servicio, podrán publicar hasta 25 tweets al día

topic    = 'esp32'
ssid     = 'LITE 3825'
password = '8Pm26?94'
api_key  = 'cVxlXTyPhZgsA6_3eB33YQd6ABdnmvC9uH35k0Isj2J'
i = 0
def isr_gpio(n):
    print(n)
    global i
    values  = {'value1':i}
    post    = {'Content-Type': 'application/json'}
    #
    request = urequests.post(
        f'https://maker.ifttt.com/trigger/{topic}/with/key/' + api_key,
        json   =values,
        headers=post)
    request.close()
    return 

def config():
    button = mn.Pin(0, mn.Pin.IN)
    button.irq(trigger=mn.Pin.IRQ_FALLING, handler=isr_gpio)
    #
    station = network.WLAN(network.STA_IF)
    #
    station.active(True)
    station.connect(ssid, password)
    #
    while station.isconnected() == False:
        pass
    #
    print('Conexión exitosa')
    print(station.ifconfig())

def main():
    config()
    global i
    while 1:
        print(f'Waiting {i}')
        time.sleep(1)
        i+=1
        if i == 10:
            i=0

if __name__ == '__main__':
    main()


