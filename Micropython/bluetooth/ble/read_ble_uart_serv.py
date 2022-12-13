#!/usr/bin/python3
# -*- coding: utf-8 -*-


from bluepy import btle

_BLE_ADDRESS     = "C8:F0:9E:9E:78:6E"

_SERVICE_UART      = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
_CHARACTERISTIC_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
_CHARACTERISTIC_TX = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

class data_driver(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
    #
    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        print(data)

def main():
    print("Conectando...")
    dev = btle.Peripheral(_BLE_ADDRESS)
    dev.setDelegate(data_driver())
    #
    service_uuid = btle.UUID(_SERVICE_UART)
    ble_service  = dev.getServiceByUUID(service_uuid)
    #
    uuidConfig = btle.UUID(_CHARACTERISTIC_RX)
    data_rx = ble_service.getCharacteristics(uuidConfig)[0]
    #
    while True:
        if dev.waitForNotifications(0.5):
            continue
        else:
            print("No hay datos nuevos")
#
if __name__ == '__main__':
    main()