#!/usr/bin/python3
# -*- coding: utf-8

from bluepy.btle import Scanner, DefaultDelegate
#
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()
    #
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Nuevo dispositivo", dev.addr)
        elif isNewData:
            print ("\tDatos recibidos", dev.addr)
#
_DEV_NAME = "EL_OMAR"
#
def main():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10)
    for dev in devices:
        info = dev.getScanData()
        if len(info)>1:
            print(info[1][2])
            if info[1][2] == _DEV_NAME:
                print(f" --> Dirección MAC: {dev.addr}")
                #40:91:51:bf:b6:7a
                break
#
if __name__ == '__main__':
    main()