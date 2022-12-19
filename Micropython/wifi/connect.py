import machine as mn
import network

import gc
gc.collect()

ssid     = 'LITE 3825'#nombre de la red
password = '8Pm26?94'

def connect():
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
    connect()

if __name__ == '__main__':
    main()

