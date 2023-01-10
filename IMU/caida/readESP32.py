import platform
import logging
import asyncio
from bleak import BleakClient
from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict

from adq import Adq_save

UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

dataFlag = False
AS = Adq_save()
d_connected = False

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    global dataFlag, AS
    AS.decode(data)
    dataFlag = True

async def connect_device(address, loop):
    global to1
    async with BleakClient(address, loop=loop) as client:
        #wait for BLE client to be connected
        x = await client.is_connected()
        print(f"Connected: {address}")
        #wait for data to be sent from client
        await client.start_notify(UART_RX_UUID, notification_handler)
        while True :
            #give some time to do other tasks
            await asyncio.sleep(0.05)
            #check if we received data
            global dataFlag
            if dataFlag :
                dataFlag = False
                data = await client.read_gatt_char(UART_RX_UUID)


if __name__ == "__main__":

    #this is MAC of our BLE device
    """
    Gera1: 08:3A:F2:B7:6C:22
    Gera2: C8:F0:9E:9E:72:DA
    """
    address1 = (
        "08:3A:F2:B7:6C:22"
    )
    address2 = (
        "C8:F0:9E:9E:72:DA"
    )

    loop = asyncio.get_event_loop()
    loop.create_task(connect_device(address2, loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
        AS.s_device()