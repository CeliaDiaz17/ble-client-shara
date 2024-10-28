import asyncio
from ble_client import BleManager  # Asegúrate de que este import sea correcto

async def main():
    ble_manager = BleManager()
    
    print("Iniciando escaneo y  conexióna dispositivos BLE...")
    await ble_manager.ble_cycle()
    
    print("\nDatos recolectados en esta ronda:")
    for address, data in ble_manager.current_round_data.items():
        print(f"Dispositivo {address}:")
        for item in data:
            print(f"  - {item}")
    
    print("\nResumen de dispositivos encontrados:")
    print(f"Total de dispositivos con el descriptor específico: {len(ble_manager.current_round_data)}")
    
    # Aquí puedes añadir más lógica si es necesario, por ejemplo:
    # - Procesar los datos recolectados
    # - Realizar acciones específicas basadas en los valores leídos
    # - Guardar los datos en un archivo o base de datos

if __name__ == "__main__":
    asyncio.run(main())
