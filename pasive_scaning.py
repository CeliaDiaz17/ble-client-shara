import asyncio
from bleak import BleakScanner, BleakClient, BleakError
import platform
import subprocess
import time

class PassiveBluetoothScanner:
    def __init__(self):
        self.connected_clients = {}  # Store connected clients
        self.data_list = []

    async def reset_bluetooth(self):
        if platform.system() == "Linux":
            try:
                print("Resetting Bluetooth adapter...")
                subprocess.run(['sudo', 'hciconfig', 'hci0', 'reset'], check=True)
                await asyncio.sleep(2)
            except subprocess.CalledProcessError as e:
                print(f"Error resetting Bluetooth: {e}")

    async def handshake(self, service_uuid="34d9a23f-2249-42a3-bb7e-6aa0640154a9", max_devices=10, scan_duration=20):
        """Establish initial Bluetooth connections with devices."""
        found_devices = set()
        connection_queue = asyncio.Queue()
        connection_locks = {}
        self.connected_clients.clear()  # Clear previous connections

        def callback(device, advertisement_data):
            service_uuids = advertisement_data.service_uuids
            if service_uuids and service_uuid in service_uuids:
                print(f"Clicker device found: {device.name} ({device.address})")
                if device.address not in found_devices:
                    found_devices.add(device.address)
                    if device.address not in connection_locks:
                        connection_locks[device.address] = asyncio.Lock()
                    asyncio.create_task(connection_queue.put((device, time.time())))
                if len(found_devices) >= max_devices:
                    print("Found enough clicker devices, stopping scan...")
                    asyncio.create_task(scanner.stop())

        async def establish_connection(device, discovery_time):
            max_retries = 3
            retry_delay = 3
            device_address = device.address

            if device_address not in connection_locks:
                connection_locks[device_address] = asyncio.Lock()

            async with connection_locks[device_address]:
                for attempt in range(max_retries):
                    try:
                        await self.reset_bluetooth()
                        print(f"Attempting connection to {device_address} (Attempt {attempt + 1}/{max_retries})")
                        client = BleakClient(device_address, timeout=10.0)
                        await client.connect()
                        
                        if client.is_connected:
                            print(f"Successfully connected to {device_address}")
                            self.connected_clients[device_address] = client
                            return
                        else:
                            print(f"Failed to establish connection with {device_address}")
                            await client.disconnect()
                    except Exception as e:
                        print(f"Connection attempt {attempt + 1} failed for {device_address}: {e}")
                        await asyncio.sleep(retry_delay)

                    if attempt == max_retries - 1:
                        print(f"Maximum connection attempts exceeded for {device_address}")

        async def process_connections():
            while True:
                try:
                    device, discovery_time = await connection_queue.get()
                    if time.time() - discovery_time < 30:
                        await establish_connection(device, discovery_time)
                    connection_queue.task_done()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error in process_connections: {e}")
                    connection_queue.task_done()

        scanner = BleakScanner(callback)

        try:
            await self.reset_bluetooth()
            await scanner.start()
            is_scanning = True
            connection_processor = asyncio.create_task(process_connections())
            await asyncio.sleep(scan_duration)
            
            if is_scanning:
                try:
                    await scanner.stop()
                except BleakError as e:
                    print(f"Error stopping scanner: {e}")
            
            is_scanning = False
            print("Handshake scan complete.")
            await connection_queue.join()
            connection_processor.cancel()
            
            try:
                await connection_processor
            except asyncio.CancelledError:
                pass
        except Exception as e:
            print(f"Error in handshake scan loop: {e}")
        finally:
            if is_scanning:
                await scanner.stop()

        return list(self.connected_clients.keys())

    async def retrieve_device_data(self):
        """Retrieve data from previously connected devices."""
        self.data_list = []
        for device_address, client in list(self.connected_clients.items()):
            try:
                if not client.is_connected:
                    await client.connect()
                
                # Use services property instead of deprecated method
                services = await client.get_services()
                services = client.services
                for service in services:
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                # Ensure we're using the current event loop
                                value = await client.read_gatt_char(char.uuid)
                                decoded_value = bytes(value).decode()
                                print(f"Characteristic {char.uuid}: {decoded_value}")
                                self.data_list.append(decoded_value)
                            except Exception as char_error:
                                print(f"Error reading characteristic {char.uuid}: {char_error}")
            except Exception as e:
                print(f"Error retrieving data from {device_address}: {e}")
                # Remove problematic client
                self.connected_clients.pop(device_address, None)
        
        return self.data_list

    async def close_connections(self):
        """Close all active Bluetooth connections."""
        for client in list(self.connected_clients.values()):
            try:
                if client.is_connected:
                    await client.disconnect()
            except Exception as e:
                print(f"Error disconnecting: {e}")
        self.connected_clients.clear()








