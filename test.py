from pasive_scaning import PassiveBluetoothScanner
import asyncio
import time

async def main():
    scanner = PassiveBluetoothScanner()
    await scanner.handshake()

    question_number = 1
    for question_number in range(1, 3):
        print("Simulating quiz question...")
        time.sleep(10)
        print("Obtaining responses to the quiz question...")
        device_responses = await scanner.retrieve_device_data()
        print(f"Obtained responses: {device_responses}")

    print("Finishing quiz...")  
    await scanner.close_connections()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())