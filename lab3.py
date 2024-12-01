from abc import ABC, abstractmethod
import math
import json
from dataclasses import dataclass, field
from unittest.mock import Mock
import unittest

# Abstract Item Class
class Item(ABC):
    def __init__(self, ID, weight, count, containerID):
        self._ID = ID
        self._weight = weight
        self._count = count
        self._containerID = containerID

    @abstractmethod
    def get_total_weight(self):
        pass

    @property
    def ID(self):
        return self._ID

    @property
    def containerID(self):
        return self._containerID

class Small(Item):
    def get_total_weight(self):
        return self._weight * self._count

class Heavy(Item):
    def get_total_weight(self):
        return self._weight * self._count

class Refrigerated(Item):
    def get_total_weight(self):
        return self._weight * self._count

class Liquid(Item):
    def get_total_weight(self):
        return self._weight * self._count

# Abstract Container Class
class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

class BasicContainer(Container):
    def consumption(self):
        return self.weight * 2.5

class HeavyContainer(Container):
    def consumption(self):
        return self.weight * 3.0

class RefrigeratedContainer(Container):
    def consumption(self):
        return self.weight * 5.0

class LiquidContainer(Container):
    def consumption(self):
        return self.weight * 4.0

# Factory Pattern for Item Creation
class ItemFactory:
    @staticmethod
    def create_item(type, ID, weight, count, containerID):
        item_classes = {
            "small": Small,
            "heavy": Heavy,
            "refrigerated": Refrigerated,
            "liquid": Liquid,
        }
        if type in item_classes:
            return item_classes[type](ID, weight, count, containerID)
        raise ValueError(f"Unknown item type: {type}")

@dataclass
class Port:
    ID: int
    latitude: float
    longitude: float
    containers: list = field(default_factory=list)
    history: list = field(default_factory=list)
    current: list = field(default_factory=list)

    def incoming_ship(self, ship):
        if ship not in self.current:
            self.current.append(ship)

    def outgoing_ship(self, ship):
        if ship in self.current:
            self.current.remove(ship)
        self.history.append(ship)

    def add_container(self, container):
        self.containers.append(container)

    def remove_container(self, container):
        if container in self.containers:
            self.containers.remove(container)

    # Calculate the distance between two ports using the haversine formula
    def get_distance(self, other_port):
        R = 6371  # Earth radius in kilometers

        # Convert latitude and longitude to radians
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_port.latitude), math.radians(other_port.longitude)

        # Calculate differences
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

# Ship Base Class and Subclasses
class Ship(ABC):
    def __init__(self, ID, fuel, current_port, total_weight_capacity, max_all_containers, fuel_per_km):
        self.ID = ID
        self.fuel = fuel
        self.current_port = current_port
        self.total_weight_capacity = total_weight_capacity
        self.max_all_containers = max_all_containers
        self.fuel_per_km = fuel_per_km
        self.containers = []

    def sail_to(self, port):
        distance = self.current_port.get_distance(port)
        total_consumption = self.fuel_per_km * distance
        if self.fuel >= total_consumption:
            self.fuel -= total_consumption
            self.current_port.outgoing_ship(self)
            port.incoming_ship(self)
            self.current_port = port
            return True
        return False

    def refuel(self, amount):
        self.fuel += amount

    def load_container(self, container):
        if (len(self.containers) < self.max_all_containers and
                sum(c.weight for c in self.containers) + container.weight <= self.total_weight_capacity):
            self.containers.append(container)
            return True
        return False

    def unload_container(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

class LightWeightShip(Ship):
    def __init__(self, ID, fuel, current_port):
        super().__init__(ID, fuel, current_port, 5000, 10, 2.0)

class MediumShip(Ship):
    def __init__(self, ID, fuel, current_port):
        super().__init__(ID, fuel, current_port, 10000, 20, 1.5)

class HeavyShip(Ship):
    def __init__(self, ID, fuel, current_port):
        super().__init__(ID, fuel, current_port, 20000, 30, 1.0)
# Builder Pattern for Ship Creation
class ShipBuilder:
    @staticmethod
    def build_ship(ship_type, ID, fuel, current_port):
        ship_types = {
            "lightweight": LightWeightShip,
            "medium": MediumShip,
            "heavy": HeavyShip,
        }
        if ship_type in ship_types:
            return ship_types[ship_type](ID, fuel, current_port)
        raise ValueError(f"Unknown ship type: {ship_type}")

# Main Class to Parse Actions and Output JSON
class PortManagementSystem:
    def __init__(self):
        self.ports = {}
        self.ships = {}
        self.containers = {}
        self.container_counter = 0

    # Process each action in the provided input list
    def run(self, actions):
        for action in actions:
            # Create a new port based on the action parameters
            if action["type"] == "create_port":
                self.create_port(action)

            # Create a new ship at a specified port
            elif action["type"] == "create_ship":
                self.create_ship(action)

            # Create a new container based on the given type and attributes
            elif action["type"] == "create_container":
                self.create_container(action)

            # Load a container onto a specified ship
            elif action["type"] == "load_container":
                self.load_container(action)

            # Unload a container from a specified ship
            elif action["type"] == "unload_container":
                self.unload_container(action)

            # Move a ship to a different port if it has enough fuel
            elif action["type"] == "sail":
                self.sail(action)

            # Refuel a ship with a specified amount
            elif action["type"] == "refuel":
                self.refuel_ship(action)

        # Generate and save the output JSON structure
        self.generate_output()

    def create_port(self, action):
        port = Port(action["ID"], action["latitude"], action["longitude"])
        self.ports[action["ID"]] = port

    def create_ship(self, action):
        port = self.ports.get(action["initial_port"])
        if port is None:
            raise ValueError(f"Initial port with ID {action['initial_port']} does not exist.")

        ship = ShipBuilder.build_ship(action["ship_type"], action["ID"], action["fuel"], port)
        port.incoming_ship(ship)
        self.ships[action["ID"]] = ship

    def create_container(self, action):
        container_types = {
            "basic": BasicContainer,
            "heavy": HeavyContainer,
            "refrigerated": RefrigeratedContainer,
            "liquid": LiquidContainer,
        }

        container_type = action.get("container_type")
        weight = action.get("weight")

        if container_type in container_types and weight is not None:
            container_class = container_types[container_type]
            container = container_class(self.container_counter, weight)
            self.containers[self.container_counter] = container
            self.container_counter += 1
        else:
            raise ValueError(f"Invalid container type '{container_type}' or missing weight.")

    # Error handling for missing ships and ports
    def load_container(self, action):
        ship = self.ships.get(action["ship_id"])
        container = self.containers.get(action["container_id"])

        if ship is None:
            raise ValueError(f"Ship with ID {action['ship_id']} does not exist.")
        if container is None:
            raise ValueError(f"Container with ID {action['container_id']} does not exist.")

        if ship.load_container(container):
            ship.current_port.containers.remove(container)

    def unload_container(self, action):
        ship = self.ships.get(action["ship_id"])
        container = self.containers.get(action["container_id"])

        if ship is None:
            raise ValueError(f"Ship with ID {action['ship_id']} does not exist.")
        if container is None:
            raise ValueError(f"Container with ID {action['container_id']} does not exist.")

        if ship.unload_container(container):
            ship.current_port.containers.append(container)

    def sail(self, action):
        ship = self.ships.get(action["ship_id"])
        destination_port = self.ports.get(action["destination_port"])

        if ship is None:
            raise ValueError(f"Ship with ID {action['ship_id']} does not exist.")
        if destination_port is None:
            raise ValueError(f"Destination port with ID {action['destination_port']} does not exist.")

        ship.sail_to(destination_port)

    def refuel_ship(self, action):
        ship = self.ships.get(action["ship_id"])
        if ship is None:
            raise ValueError(f"Ship with ID {action['ship_id']} does not exist.")

        ship.refuel(action["amount"])

    def generate_output(self):
        output = {
            f"Port {port.ID}": {
                "containers": [c.ID for c in port.containers],
                "ships": [ship.ID for ship in port.current]
            } for port in self.ports.values()
        }
        with open('output.json', 'w') as f:
            json.dump(output, f, indent=4)

# Tests (extended)
class TestPortManagementSystem(unittest.TestCase):
    def setUp(self):
        self.mock_ship = Mock()
        self.mock_port = Port(1, 10.0, 20.0)
        self.mock_port.incoming_ship(self.mock_ship)

    def test_incoming_ship(self):
        self.assertIn(self.mock_ship, self.mock_port.current)

    def test_outgoing_ship(self):
        self.mock_port.outgoing_ship(self.mock_ship)
        self.assertNotIn(self.mock_ship, self.mock_port.current)
        self.assertIn(self.mock_ship, self.mock_port.history)

    def test_item_creation(self):
        item = ItemFactory.create_item("small", 1, 10.0, 5, "C1")
        self.assertEqual(item.get_total_weight(), 50.0)

    def test_distance_calculation(self):
        port1 = Port(1, 10.0, 20.0)
        port2 = Port(2, 10.5, 21.0)
        self.assertAlmostEqual(port1.get_distance(port2), haversine(10.0, 20.0, 10.5, 21.0), places=2)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

if __name__ == "__main__":
    unittest.main()
