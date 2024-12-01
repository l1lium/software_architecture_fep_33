from typing import List, Union
import math
import json

# Abstract classes
class IPort:
    def incomingShip(self, ship: 'Ship'):
        raise NotImplementedError

    def outgoingShip(self, ship: 'Ship'):
        raise NotImplementedError

class IShip:
    def sailTo(self, port: 'Port') -> bool:
        raise NotImplementedError

    def reFuel(self, fuel: float):
        raise NotImplementedError

    def load(self, container: 'Container') -> bool:
        raise NotImplementedError

    def unLoad(self, container: 'Container') -> bool:
        raise NotImplementedError

# Base classes
class Container:
    def __init__(self, ID: int, weight: int):
        self.ID = ID
        self.weight = weight

    def consumption(self) -> float:
        raise NotImplementedError

    def equals(self, other: 'Container') -> bool:
        return (
            isinstance(other, Container)
            and self.ID == other.ID
            and self.weight == other.weight
        )

class BasicContainer(Container):
    def consumption(self) -> float:
        return self.weight * 2.5

class HeavyContainer(Container):
    def consumption(self) -> float:
        return self.weight * 3.0

class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 5.0

class LiquidContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 4.0

class Port(IPort):
    def __init__(self, ID: int, latitude: float, longitude: float):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers: List[Container] = []
        self.history: List['Ship'] = []
        self.current: List['Ship'] = []

    def incomingShip(self, ship: 'Ship'):
        if ship not in self.current:
            self.current.append(ship)
            if ship not in self.history:
                self.history.append(ship)

    def outgoingShip(self, ship: 'Ship'):
        if ship in self.current:
            self.current.remove(ship)

    def getDistance(self, other: 'Port') -> float:
        # Haversine formula for distance
        R = 6371  # Earth's radius in km
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

class Ship(IShip):
    def __init__(
        self,
        ID: int,
        fuel: float,
        currentPort: Port,
        totalWeightCapacity: int,
        maxNumberOfAllContainers: int,
        maxNumberOfHeavyContainers: int,
        maxNumberOfRefrigeratedContainers: int,
        maxNumberOfLiquidContainers: int,
        fuelConsumptionPerKM: float,
    ):
        self.ID = ID
        self.fuel = fuel
        self.currentPort = currentPort
        self.totalWeightCapacity = totalWeightCapacity
        self.maxNumberOfAllContainers = maxNumberOfAllContainers
        self.maxNumberOfHeavyContainers = maxNumberOfHeavyContainers
        self.maxNumberOfRefrigeratedContainers = maxNumberOfRefrigeratedContainers
        self.maxNumberOfLiquidContainers = maxNumberOfLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.containers: List[Container] = []

    def sailTo(self, port: Port) -> bool:
        distance = self.currentPort.getDistance(port)
        totalConsumption = distance * self.fuelConsumptionPerKM + sum(c.consumption() for c in self.containers)
        if self.fuel >= totalConsumption:
            self.fuel -= totalConsumption
            self.currentPort.outgoingShip(self)
            port.incomingShip(self)
            self.currentPort = port
            return True
        return False

    def reFuel(self, fuel: float):
        self.fuel += fuel

    def load(self, container: Container) -> bool:
        if len(self.containers) >= self.maxNumberOfAllContainers or sum(c.weight for c in self.containers) + container.weight > self.totalWeightCapacity:
            return False
        if isinstance(container, HeavyContainer) and len([c for c in self.containers if isinstance(c, HeavyContainer)]) >= self.maxNumberOfHeavyContainers:
            return False
        if isinstance(container, RefrigeratedContainer) and len([c for c in self.containers if isinstance(c, RefrigeratedContainer)]) >= self.maxNumberOfRefrigeratedContainers:
            return False
        if isinstance(container, LiquidContainer) and len([c for c in self.containers if isinstance(c, LiquidContainer)]) >= self.maxNumberOfLiquidContainers:
            return False

        self.containers.append(container)
        return True

    def unLoad(self, container: Container) -> bool:
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

    def getCurrentContainers(self) -> List[Container]:
        return sorted(self.containers, key=lambda c: c.ID)

# JSON Parsing and Main Logic
def parse_json(input_file: str):
    with open(input_file, 'r') as file:
        return json.load(file)

def main(input_file: str, output_file: str):
    data = parse_json(input_file)

    ports = {int(port['ID']): Port(port['ID'], port['latitude'], port['longitude']) for port in data['ports']}
    ships = {}
    containers = {}

    for container_data in data['containers']:
        ID = container_data['ID']
        weight = container_data['weight']
        if container_data['type'] == 'Basic':
            containers[ID] = BasicContainer(ID, weight)
        elif container_data['type'] == 'Heavy':
            containers[ID] = HeavyContainer(ID, weight)
        elif container_data['type'] == 'Refrigerated':
            containers[ID] = RefrigeratedContainer(ID, weight)
        elif container_data['type'] == 'Liquid':
            containers[ID] = LiquidContainer(ID, weight)

    for ship_data in data['ships']:
        ID = ship_data['ID']
        currentPort = ports[ship_data['currentPortID']]
        ships[ID] = Ship(
            ID,
            ship_data['fuel'],
            currentPort,
            ship_data['totalWeightCapacity'],
            ship_data['maxNumberOfAllContainers'],
            ship_data['maxNumberOfHeavyContainers'],
            ship_data['maxNumberOfRefrigeratedContainers'],
            ship_data['maxNumberOfLiquidContainers'],
            ship_data['fuelConsumptionPerKM'],
        )
        currentPort.incomingShip(ships[ID])

    for action in data['actions']:
        if action['type'] == 'load':
            ship = ships[action['shipID']]
            container = containers[action['containerID']]
            success = ship.load(container)
            if success:
                ports[ship.currentPort.ID].containers.remove(container)

        elif action['type'] == 'unload':
            ship = ships[action['shipID']]
            container = containers[action['containerID']]
            success = ship.unLoad(container)
            if success:
                ports[ship.currentPort.ID].containers.append(container)

        elif action['type'] == 'sail':
            ship = ships[action['shipID']]
            destination = ports[action['destinationPortID']]
            ship.sailTo(destination)

        elif action['type'] == 'refuel':
            ship = ships[action['shipID']]
            ship.reFuel(action['amount'])

    output = {}
    for port in sorted(ports.values(), key=lambda p: p.ID):
        output[f"Port {port.ID}"] = {
            "lat": round(port.latitude, 2),
            "lon": round(port.longitude, 2),
            "containers": [container.ID for container in port.containers],
            "ships": {ship.ID: {"fuel_left": round(ship.fuel, 2), "containers": [c.ID for c in ship.getCurrentContainers()]} for ship in port.current}
        }

