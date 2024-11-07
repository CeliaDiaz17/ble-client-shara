from pasive_scaning import PassiveBluetoothScanner
import asyncio

scanner = PassiveBluetoothScanner()
data_list = asyncio.run(scanner.scan_devices())
print(f"Final data list: {data_list}")