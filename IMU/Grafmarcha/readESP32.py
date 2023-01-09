import platform
import logging
import asyncio
from bleak import BleakClient
from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict

"""
    Gera1: 08:3A:F2:B7:6C:22
    Gera2: C8:F0:9E:9E:72:DA
"""

class YomuESP32():
    def __init__(self, AS):
        self.UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
        self.UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX
        self.dataFlag = False
        self.AS = AS
        self.d1_connected = False
        self.d2_connected = False
        self.c_address = ""
        self.to1=float()
        self.to2=float()
        self.desfase_adq = 0
        self.loop = asyncio.get_event_loop()
        
    def start(self):
        address1 = ("08:3A:F2:B7:6C:22")
        address2 = ("C8:F0:9E:9E:72:DA")
        self.loop.create_task(connect_device1(address1, loop))
        self.loop.create_task(connect_device2(address2, loop))
        self.loop.run_forever()
    #
    def stop(self):
        print(f"desfase_adq: {to2-to1}")
        self.loop.stop()
        self.AS.s_device1()
        self.AS.s_device2()
    #
    def notification_handler(self,sender, data):
        """Simple notification handler which prints the data received."""
        #print(f"{c_address}: {data}")
        self.AS.decode(data, self.c_address)
        self.dataFlag = True
    #
    async def connect_device1(self, address, loop):
        async with BleakClient(address, loop=loop) as client:
            #wait for BLE client to be connected
            x = await client.is_connected()
            print(f"Connected: {address}")
            self.to1 = time()
            #wait for data to be sent from client
            await client.start_notify(UART_RX_UUID, notification_handler)
            while True :
                #give some time to do other tasks
                await asyncio.sleep(0.05)
                #check if we received data
                if dataFlag :
                    self.dataFlag = False
                    self.c_address = address
                    data = await client.read_gatt_char(UART_RX_UUID)
    #
    async def connect_device2(self, address, loop):
        await asyncio.sleep(10)
        async with BleakClient(address, loop=loop) as client:
            #wait for BLE client to be connected
            x = await client.is_connected()
            print(f"Connected: {address}")
            self.to2 = time()
            #wait for data to be sent from client
            await client.start_notify(UART_RX_UUID, notification_handler)
            while True :
                #give some time to do other tasks
                await asyncio.sleep(0.05)
                #check if we received data
                if dataFlag :
                    self.dataFlag = False
                    self.c_address = address
                    data = await client.read_gatt_char(UART_RX_UUID)

