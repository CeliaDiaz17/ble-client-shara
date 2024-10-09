'''
Based on: https://github.com/hbldh/bleak/tree/develop/examples 
This class is designed to connect to a BLE device and read its services and features.
In addition, a queue has been implemented to store the read values of the features.
'''
import asyncio
from bleak import BleakClient, BleakScanner
from queue import Queue
import json
import os

class BleManager:
    def __init__(self):    
        self.address_1 = "14:2B:2F:B0:70:C2"
        self.address_2 = "10:06:1c:27:6e:a2"
        self.address_3 = "10:06:1c:28:63:76"
        self.address_queue = Queue()
        for address in [self.address_1, self.address_2, self.address_3]:
            self.address_queue.put(address)

        self.MAX_RECONNECT = 5 #pq en el quiz hay 5 preguntas :D
        self.OUTPUT_DIR = "respuestas"
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        
        self.current_round_data = {}

    async def scan_device(self,address):
        max_retries =  10 #num max de intentos de reconexion si alguno falla
        data_list = []
        connected = False
        for attempt in range(max_retries):
            try:
                async with BleakClient(address) as client:
                    print(f"Connected to: {address}")
                    x = await client.is_connected()
                    services = await client.get_services()
                    for service in services:
                        for char in service.characteristics:
                            if "read" in char.properties:
                                value = bytes(await client.read_gatt_char(char.uuid))
                                decoded_value = value.decode()
                                print(f"Characteristic: {char.description} ({char.uuid}) | Value: {decoded_value}")
                                data_list.append(decoded_value)
                    await client.disconnect()
                    connected = True
                    break
            except Exception as e:
                print(f"Error al conectar con {address}: {str(e)}")
                if attempt == max_retries - 1:
                    print(f"Se ha superado el número máximo de intentos para conectar con {address}.")
                else:
                    print(f"Reintentando la conexión con {address}...")
        return data_list

    async def ble_cycle(self):
        round_data = {}
            
        temp_queue = Queue()
        while not self.address_queue.empty():
            address = self.address_queue.get()
            device_data = await self.scan_device(address)
            round_data[address] = device_data
            temp_queue.put(address)
            
            # Restaurar la cola de direcciones
        while not temp_queue.empty():
            self.address_queue.put(temp_queue.get())
            
        self.current_round_data = round_data
        print("Ronda de conexiones completada. Datos almacenados en la lista.")
            
                    
