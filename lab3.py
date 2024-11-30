import math
import json
from abc import ABC, abstractmethod


# --- Interfaces ---
class IPort(ABC):
    @abstractmethod
    def incoming_ship(self, ship):
        pass

    @abstractmethod
    def outgoing_ship(self, ship):
        pass


class IShip(ABC):
    @abstractmethod
    def sail_to(self, port):
        pass

    @abstractmethod
    def refuel(self, fuel_amount):
        pass

    @abstractmethod
    def load(self, container):
        pass

    @abstractmethod
    def unload(self, container):
        pass


# --- Containers ---
class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Container) and self.ID == other.ID and self.weight == other.weight


class BasicContainer(Container):
    def consumption(self):
        return self.weight * 2.5


class HeavyContainer(Container):
    def consumption(self):
        return self.weight * 3.0


class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return self.weight * 5.0


class LiquidContainer(HeavyContainer):
    def consumption(self):
        return self.weight * 4.0


# --- Container Factory ---
class ContainerFactory:
    @staticmethod
    def create_container(container_type, ID, weight):
        if container_type == "Basic":
            return BasicContainer(ID, weight)
        elif container_type == "Heavy":
            return HeavyContainer(ID, weight)
        elif container_type == "Refrigerated":
            return RefrigeratedContainer(ID, weight)
        elif container_type == "Liquid":
            return LiquidContainer(ID, weight)
        else:
            raise ValueError(f"Unknown container type: {container_type}")


# --- Ports ---
class Port(IPort):
    def __init__(self, ID, latitude, longitude):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current = []

    def get_distance(self, other):
        return math.sqrt((self.latitude - other.latitude)**2 + (self.longitude - other.longitude)**2)

    def incoming_ship(self, ship):
        if ship not in self.current:
            self.current.append(ship)
        if ship not in self.history:
            self.history.append(ship)

    def outgoing_ship(self, ship):
        if ship in self.current:
            self.current.remove(ship)


# --- Ships ---
class Ship(IShip):
    def __init__(self, ID, fuel, total_weight_capacity, max_containers, fuel_per_km):
        self.ID = ID
        self.fuel = fuel
        self.total_weight_capacity = total_weight_capacity
        self.max_containers = max_containers
        self.fuel_per_km = fuel_per_km
        self.current_port = None
        self.containers = []

    def sail_to(self, port):
        if self.current_port is None:
            raise ValueError("The ship is not in any port.")
        distance = self.current_port.get_distance(port)
        required_fuel = self.fuel_per_km * distance + sum(c.consumption() * distance for c in self.containers)
        if self.fuel >= required_fuel:
            self.fuel -= required_fuel
            self.current_port.outgoing_ship(self)
            self.current_port = port
            port.incoming_ship(self)
            return True
        return False

    def refuel(self, fuel_amount):
        self.fuel += fuel_amount

    def load(self, container):
        if len(self.containers) < self.max_containers and self.total_weight_capacity >= sum(c.weight for c in self.containers) + container.weight:
            self.containers.append(container)
            return True
        return False

    def unload(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False


# --- Ship Types ---
class LightWeightShip(Ship):
    def __init__(self, ID, fuel):
        super().__init__(ID, fuel, total_weight_capacity=1000, max_containers=10, fuel_per_km=1.0)


class MediumShip(Ship):
    def __init__(self, ID, fuel):
        super().__init__(ID, fuel, total_weight_capacity=5000, max_containers=30, fuel_per_km=2.0)


class HeavyShip(Ship):
    def __init__(self, ID, fuel):
        super().__init__(ID, fuel, total_weight_capacity=20000, max_containers=50, fuel_per_km=3.5)


# --- Ship Factory ---
class ShipFactory:
    @staticmethod
    def create_ship(ship_type, ID, fuel):
        if ship_type == "LightWeight":
            return LightWeightShip(ID, fuel)
        elif ship_type == "Medium":
            return MediumShip(ID, fuel)
        elif ship_type == "Heavy":
            return HeavyShip(ID, fuel)
        else:
            raise ValueError(f"Unknown ship type: {ship_type}")


# --- Main Program ---
def main(input_json):
    data = json.loads(input_json)

    # Create ports
    ports = {}
    for port_data in data["ports"]:
        ports[port_data["ID"]] = Port(port_data["ID"], port_data["latitude"], port_data["longitude"])

    # Create ships
    ships = {}
    for ship_data in data["ships"]:
        ships[ship_data["ID"]] = ShipFactory.create_ship(ship_data["type"], ship_data["ID"], ship_data["fuel"])

    # Create containers
    containers = {}
    for cont_data in data["containers"]:
        containers[cont_data["ID"]] = ContainerFactory.create_container(cont_data["type"], cont_data["ID"], cont_data["weight"])

    # Simulate actions
    # Example: Process actions from the input...

    # Output results
    output = {}
    for port_id, port in ports.items():
        output[f"Port {port_id}"] = {
            "lat": round(port.latitude, 2),
            "lon": round(port.longitude, 2),
            "ships": [ship.ID for ship in port.current]
        }
    print(json.dumps(output, indent=2))


# --- Example Input ---
input_json = '''
{
    "ports": [{"ID": 1, "latitude": 50.0, "longitude": 30.0}],
    "ships": [{"ID": 1, "type": "Medium", "fuel": 500}],
    "containers": [{"ID": 1, "type": "Basic", "weight": 1000}]
}
'''
main(input_json)
