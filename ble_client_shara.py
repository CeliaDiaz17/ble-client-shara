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

address_1 = "14:2B:2F:B0:70:C2"
address_2 = "10:06:1c:27:6e:a2"
address_3 = "10:06:1c:28:63:76"
address_queue = Queue()
for address in [address_1, address_2, address_3]:
    address_queue.put(address)
    
data_list = []

RECONNECT_INTERVAL = 20 #Cambiar al tiempo que se tarde en una pregunta
MAX_RECONNECT = 5 #pq en el quiz hay 5 preguntas :D
OUTPUT_DIR = "respuestas"

async def scan_device(address):
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

async def main():
    reconnect_count = 0
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    while reconnect_count < MAX_RECONNECT:
        print(f"Iniciando nueva ronda de conexiones (Pregunta {reconnect_count + 1})...")
        round_data = {}
        
        # Reiniciar la lista de datos antes de la nueva ronda de conexiones
        data_list = []
        
        temp_queue = Queue()
        while not address_queue.empty():
            address = address_queue.get()
            device_data = await scan_device(address)
            round_data[address] = device_data
            temp_queue.put(address)
        
        # Restaurar la cola de direcciones
        while not temp_queue.empty():
            address_queue.put(temp_queue.get())
        
        print("Ronda de conexiones completada. Datos almacenados en la lista.")
        
        # Guardar los datos en un archivo JSON
        filename = os.path.join(OUTPUT_DIR, f"respuestas_pregunta_{reconnect_count + 1}.json")
        with open(filename, "w") as file:
            json.dump(round_data, file, indent=2)        
        print(f"Datos guardados en '{filename}'")
        
        reconnect_count += 1
        
        if reconnect_count < MAX_RECONNECT:
            print(f"Esperando {RECONNECT_INTERVAL} segundos antes de la próxima ronda de conexiones...")
            await asyncio.sleep(RECONNECT_INTERVAL)
        
        print("Proceso completado. Se han guardado todas las respuestas")

# Ejecutar el programa
if __name__ == "__main__":
    asyncio.run(main())