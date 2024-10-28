import asyncio
from bleak import BleakScanner, BleakClient, BleakError
import platform
import subprocess
import time

async def scan_devices():
    print("Starting passive scan...")
    found_clicker_queue = set()
    connection_queue = asyncio.Queue()
    connection_locks = {}
    global data_list
    data_list = []
    is_scanning = False

    async def reset_bluetooth():
        if platform.system() == "Linux":
            try:
                print("Resetting Bluetooth adapter...")
                subprocess.run(['sudo', 'hciconfig', 'hci0', 'reset'], check=True)
                await asyncio.sleep(2)
            except subprocess.CalledProcessError as e:
                print(f"Error resetting Bluetooth: {e}")
    
    def callback(device, advertisement_data):
        matching_service_uuid = "34d9a23f-2249-42a3-bb7e-6aa0640154a9"
        service_uuids = advertisement_data.service_uuids
        
        if service_uuids and matching_service_uuid in service_uuids:
            print(f"Clicker device found: {device.name} ({device.address})")
            if device.address not in found_clicker_queue:
                found_clicker_queue.add(device.address)
                if device.address not in connection_locks:
                    connection_locks[device.address] = asyncio.Lock()
                asyncio.create_task(connection_queue.put((device, time.time())))
                
            if len(found_clicker_queue) >= 2:
                print("Found enough clicker devices, stopping scan...")
                asyncio.create_task(scanner.stop())

    async def connect_to_device(device, discovery_time):
        max_retries = 3
        retry_delay = 3
        device_address = device.address

        if device_address not in connection_locks:
            connection_locks[device_address] = asyncio.Lock()

        async with connection_locks[device_address]:
            for attempt in range(max_retries):
                try:
                    await reset_bluetooth()
                    print(f"Attempting connection to {device_address} (Attempt {attempt + 1}/{max_retries})")
                    
                    verification_scanner = BleakScanner()
                    await verification_scanner.start()
                    await asyncio.sleep(2)
                    devices = verification_scanner.discovered_devices
                    await verification_scanner.stop()

                    if not any(d.address == device_address for d in devices):
                        print(f"Device {device_address} not found in scan")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(retry_delay)
                        continue

                    async with BleakClient(device_address, timeout=10.0) as client:
                        if client.is_connected:
                            print(f"Successfully connected to {device_address}")
                            services = await client.get_services()
                            
                            for service in services:
                                for char in service.characteristics:
                                    if "read" in char.properties:
                                        try:
                                            value = bytes(await client.read_gatt_char(char.uuid))
                                            decoded_value = value.decode()
                                            print(f"Characteristic {char.uuid}: {decoded_value}")
                                            # Agregar el valor a `data_list` (ahora global)
                                            data_list.append((decoded_value))
                                        except Exception as char_error:
                                            print(f"Error reading characteristic {char.uuid}: {char_error}")
                            return
                        else:
                            print(f"Failed to establish connection with {device_address}")
                            
                except Exception as e:
                    print(f"Connection attempt {attempt + 1} failed for {device_address}: {e}")
                    if "Operation already in progress" in str(e):
                        print("Detected 'Operation in progress', resetting Bluetooth...")
                        await reset_bluetooth()
                        await asyncio.sleep(retry_delay * 2)
                    else:
                        await asyncio.sleep(retry_delay)

                if attempt == max_retries - 1:
                    print(f"Maximum connection attempts exceeded for {device_address}")
                else:
                    print(f"Retrying connection to {device_address}...")

    async def process_connections():
        while True:
            try:
                device, discovery_time = await connection_queue.get()
                if time.time() - discovery_time < 30:
                    await connect_to_device(device, discovery_time)
                connection_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in process_connections: {e}")
                connection_queue.task_done()

    scanner = BleakScanner(callback)
    
    try:
        await reset_bluetooth()
        await scanner.start()
        is_scanning = True
        connection_processor = asyncio.create_task(process_connections())
        
        await asyncio.sleep(20)
        
        if is_scanning:
            try:
                await scanner.stop()
            except BleakError as e:
                print(f"Error stopping scanner: {e}")
            is_scanning = False
            
        print("Scan complete.")
        
        await connection_queue.join()
        connection_processor.cancel()
        try:
            await connection_processor
        except asyncio.CancelledError:
            pass
        
        print(f"Final data list: {data_list}")
    
    except Exception as e:
        print(f"Error in main scan loop: {e}")
    finally:
        if is_scanning:
            await scanner.stop()

if __name__ == "__main__":
    asyncio.run(scan_devices())


