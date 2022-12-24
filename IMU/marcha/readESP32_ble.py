import platform
import logging
import asyncio
from bleak import BleakClient
from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict

UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

dataFlag = False

c_address = ""

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    global dataFlag, c_address
    print(f"{c_address}: {data}")
    dataFlag = True

async def connect_device1(address, loop,):

    async with BleakClient(address, loop=loop) as client:
        #wait for BLE client to be connected
        x = await client.is_connected()
        print(f"Connected: {address}")
        #wait for data to be sent from client
        await client.start_notify(UART_RX_UUID, notification_handler)
        while True :
            #give some time to do other tasks
            await asyncio.sleep(0.045)
            #check if we received data
            global dataFlag, c_address
            if dataFlag :
                dataFlag = False
                c_address = address
                data = await client.read_gatt_char(UART_RX_UUID)

async def connect_device2(address, loop):

    async with BleakClient(address, loop=loop) as client:
        #wait for BLE client to be connected
        x = await client.is_connected()
        print(f"Connected: {address}")
        #wait for data to be sent from client
        await client.start_notify(UART_RX_UUID, notification_handler)
        while True :
            #give some time to do other tasks
            await asyncio.sleep(0.1)
            #check if we received data
            global dataFlag, c_address
            if dataFlag :
                dataFlag = False
                c_address = address
                data = await client.read_gatt_char(UART_RX_UUID)


if __name__ == "__main__":

    #this is MAC of our BLE device
    """
    Gera1: C8:F0:9E:9E:78:6E
    Gera2: C8:F0:9E:9E:72:DA
    """
    address1 = (
        "C8:F0:9E:9E:78:6E"
    )
    address2 = (
        "C8:F0:9E:9E:72:DA"
    )

    loop = asyncio.get_event_loop()
    loop.create_task(connect_device1(address1, loop))
    loop.create_task(connect_device2(address2, loop))
    try:
        loop.run_forever()
    except (KeyboardInterrupt, BleakDeviceNotFoundError):
        loop.stop()