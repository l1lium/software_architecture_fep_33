import json
from classes import *

# Зчитуємо вхідний JSON файл
def load_input_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Записуємо вихідний JSON файл
def write_output_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Створення об'єктів з JSON даних
def create_ports(data):
    ports = {}
    for port_data in data['ports']:
        port = Port(port_data['ID'], port_data['latitude'], port_data['longitude'])
        ports[port.ID] = port
    return ports

def create_ships(data, ports):
    ships = {}
    for ship_data in data['ships']:
        port = ports[ship_data['currentPortID']]
        ship = Ship(
            ship_data['ID'],
            ship_data['fuel'],
            port,
            ship_data['totalWeightCapacity'],
            ship_data['maxNumContainers'],
            ship_data['maxHeavyContainers'],
            ship_data['maxRefrigeratedContainers'],
            ship_data['maxLiquidContainers'],
            ship_data['fuelConsumptionPerKM']
        )
        ships[ship.ID] = ship
        port.incomingShip(ship)
    return ships

# Основний цикл програми
def main():
    data = load_input_data('data/input.json')
    ports = create_ports(data)
    ships = create_ships(data, ports)

    # Виведення інформації про порти та кораблі
    print("Ports:")
    for port in ports.values():
        print(f"Port {port.ID}: Latitude {port.latitude}, Longitude {port.longitude}")
        print(f"  Containers at port: {len(port.containers)}")
        print(f"  Ships at port: {len(port.current)}")

    print("\nShips:")
    for ship in ships.values():
        print(f"Ship {ship.ID}: Fuel {ship.fuel}")
        print(f"  Containers on ship: {len(ship.containers)}")

    # Пишемо результат у файл
    write_output_data('data/output.json', data)

if __name__ == '__main__':
    main()