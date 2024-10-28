'''
Based on: https://github.com/hbldh/bleak/tree/develop/examples 
This class is designed to connect to a BLE device and read its services and features.
In addition, a queue has been implemented to store the devices values.
'''

from bleak import BleakClient, BleakScanner
import asyncio

class BleManager:
    def __init__(self):    
        self.MAX_RECONNECT = 5 #num max de intentos de reconexion si alguno falla
        self.current_round_data = {}
    
    async def scan_device(self, device):
        data_list = []
        try:
            print(f"Scanning device: {device.name} ({device.address})")
            async with BleakClient(device, timeout=20) as client:
                services = await client.get_services()
                is_clicker = False
                for service in services:
                    for char in service.characteristics:
                        if char.descriptors:
                            for descriptor in char.descriptors:
                                descriptor_val = await client.read_gatt_descriptor(descriptor.handle)
                                try:
                                    decoded_desc = descriptor_val.decode('utf-8')
                                    print(f"Descriptor: {decoded_desc}")
                                    if "clicker" in decoded_desc.lower():
                                        print(f"Clicker device found: {device.name} ({device.address})")
                                        is_clicker = True    
                                        break
                                    
                                except UnicodeDecodeError:
                                    print(f"Descriptor contains binary data: {descriptor_val}")
                        if is_clicker:
                            break
                    if is_clicker:
                        break
                
                if is_clicker:
                    print(f"Collecting data from {device.name} ({device.address})")
                    for service in services:
                        for char in service.characteristics:
                            if "read" in char.properties:
                                value = bytes(await client.read_gatt_char(char.uuid))
                                decoded_value = value.decode(errors="ignore")
                                print(f"Characteristic: {char.description} ({char.uuid}) | Value: {decoded_value}")
                                data_list.append(decoded_value)
        except Exception as e:    
            print(f"Error while scanning or connecting to {device.name} ({device.address}): {e}")
        
        print(f"Data collected: {data_list}")
        return data_list

    #TODO quitar lo del numero de clickers para produccion, no es necesario
    async def ble_cycle(self):
        clicker_values = [] 
        max_retries = 1 #TODO: modificar si es necesario. Lo dejo asi para tardar menos en probar.
        
        for attempt in range(max_retries):
            round_data = {}
            print(f"Scan attempt {attempt + 1}")
            devices = await BleakScanner.discover(timeout=30)
            print(f"Devices found: {len(devices)}")
            
            if not devices:
                print("No devices found")
                continue
            
            clicker_count = 0
            for device in devices:
                try:
                    device_data = await self.scan_device(device)
                    if device_data:
                        clicker_values.append(device_data)
                        clicker_count += 1
                except Exception as e:
                    print(f"Error scanning {device.name}: {e}")
            
            if clicker_values:
                print(f"Found {len(clicker_values)} clicker values: {clicker_values}.")
            
            print(f"Found {clicker_count} clicker devices in this scan.")
            if clicker_count == 7:
                self.current_round_data = round_data
                print("Connection round terminated. Data has been stored.")
                return
            else:
                print(f"Expected {7} clickers, but found {clicker_count}. Retrying...")
                await asyncio.sleep(2)  # Wait before retrying
        
        print(f"Failed to find {7} clickers after {max_retries} attempts.")
        self.current_round_data = round_data  # Store the data from the last attempt
                    
