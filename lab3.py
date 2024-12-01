from abc import ABC, abstractmethod
import math
import json
from dataclasses import dataclass, field
from unittest.mock import Mock
import unittest

# Abstract Base Class for Item
class Product(ABC):
    def __init__(self, product_id, weight, quantity, container_id):
        self._product_id = product_id
        self._weight = weight
        self._quantity = quantity
        self._container_id = container_id

    @abstractmethod
    def get_total_weight(self):
        pass

    @property
    def product_id(self):
        return self._product_id

    @property
    def container_id(self):
        return self._container_id

class SmallProduct(Product):
    def get_total_weight(self):
        return self._weight * self._quantity

class HeavyProduct(Product):
    def get_total_weight(self):
        return self._weight * self._quantity

class RefrigeratedProduct(Product):
    def get_total_weight(self):
        return self._weight * self._quantity

class LiquidProduct(Product):
    def get_total_weight(self):
        return self._weight * self._quantity

# Abstract Base Class for Container
class StorageContainer(ABC):
    def __init__(self, container_id, weight):
        self.container_id = container_id
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

class BasicStorage(StorageContainer):
    def consumption(self):
        return self.weight * 2.5

class HeavyStorage(StorageContainer):
    def consumption(self):
        return self.weight * 3.0

class RefrigeratedStorage(StorageContainer):
    def consumption(self):
        return self.weight * 5.0

class LiquidStorage(StorageContainer):
    def consumption(self):
        return self.weight * 4.0

# Factory for Creating Product Instances
class ProductFactory:
    @staticmethod
    def create_product(product_type, product_id, weight, quantity, container_id):
        product_classes = {
            "small": SmallProduct,
            "heavy": HeavyProduct,
            "refrigerated": RefrigeratedProduct,
            "liquid": LiquidProduct,
        }
        if product_type in product_classes:
            return product_classes[product_type](product_id, weight, quantity, container_id)
        raise ValueError(f"Unknown product type: {product_type}")

@dataclass
class Harbor:
    harbor_id: int
    latitude: float
    longitude: float
    containers: list = field(default_factory=list)
    history: list = field(default_factory=list)
    active_ships: list = field(default_factory=list)

    def incoming_vessel(self, ship):
        if ship not in self.active_ships:
            self.active_ships.append(ship)

    def outgoing_vessel(self, ship):
        if ship in self.active_ships:
            self.active_ships.remove(ship)
        self.history.append(ship)

    def add_storage(self, container):
        self.containers.append(container)

    def remove_storage(self, container):
        if container in self.containers:
            self.containers.remove(container)

    # Calculate the distance between two harbors using the haversine formula
    def calculate_distance(self, other_harbor):
        R = 6371  # Earth radius in kilometers

        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_harbor.latitude), math.radians(other_harbor.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

# Ship Class and Subclasses
class Vessel(ABC):
    def __init__(self, vessel_id, fuel, current_harbor, capacity, max_containers, fuel_per_km):
        self.vessel_id = vessel_id
        self.fuel = fuel
        self.current_harbor = current_harbor
        self.capacity = capacity
        self.max_containers = max_containers
        self.fuel_per_km = fuel_per_km
        self.containers = []

    def navigate_to(self, harbor):
        distance = self.current_harbor.calculate_distance(harbor)
        total_fuel = self.fuel_per_km * distance
        if self.fuel >= total_fuel:
            self.fuel -= total_fuel
            self.current_harbor.outgoing_vessel(self)
            harbor.incoming_vessel(self)
            self.current_harbor = harbor
            return True
        return False

    def refuel(self, amount):
        self.fuel += amount

    def load_storage(self, container):
        if (len(self.containers) < self.max_containers and
                sum(c.weight for c in self.containers) + container.weight <= self.capacity):
            self.containers.append(container)
            return True
        return False

    def unload_storage(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

class LightVessel(Vessel):
    def __init__(self, vessel_id, fuel, current_harbor):
        super().__init__(vessel_id, fuel, current_harbor, 5000, 10, 2.0)

class MediumVessel(Vessel):
    def __init__(self, vessel_id, fuel, current_harbor):
        super().__init__(vessel_id, fuel, current_harbor, 10000, 20, 1.5)

class HeavyVessel(Vessel):
    def __init__(self, vessel_id, fuel, current_harbor):
        super().__init__(vessel_id, fuel, current_harbor, 20000, 30, 1.0)

# Ship Builder
class VesselBuilder:
    @staticmethod
    def build_vessel(vessel_type, vessel_id, fuel, current_harbor):
        vessel_types = {
            "light": LightVessel,
            "medium": MediumVessel,
            "heavy": HeavyVessel,
        }
        if vessel_type in vessel_types:
            return vessel_types[vessel_type](vessel_id, fuel, current_harbor)
        raise ValueError(f"Unknown vessel type: {vessel_type}")

# Main Port Management System
class HarborManagementSystem:
    def __init__(self):
        self.harbors = {}
        self.vessels = {}
        self.storages = {}
        self.storage_counter = 0

    def execute_actions(self, actions):
        for action in actions:
            if action["type"] == "create_harbor":
                self.create_harbor(action)
            elif action["type"] == "create_vessel":
                self.create_vessel(action)
            elif action["type"] == "create_storage":
                self.create_storage(action)
            elif action["type"] == "load_storage":
                self.load_storage(action)
            elif action["type"] == "unload_storage":
                self.unload_storage(action)
            elif action["type"] == "navigate":
                self.navigate(action)
            elif action["type"] == "refuel":
                self.refuel_vessel(action)

        self.generate_json_output()

    def create_harbor(self, action):
        harbor = Harbor(action["ID"], action["latitude"], action["longitude"])
        self.harbors[action["ID"]] = harbor

    def create_vessel(self, action):
        harbor = self.harbors.get(action["initial_harbor"])
        if harbor is None:
            raise ValueError(f"Initial harbor with ID {action['initial_harbor']} does not exist.")
        vessel = VesselBuilder.build_vessel(action["vessel_type"], action["ID"], action["fuel"], harbor)
        harbor.incoming_vessel(vessel)
        self.vessels[action["ID"]] = vessel

    def create_storage(self, action):
        container_types = {
            "basic": BasicStorage,
            "heavy": HeavyStorage,
            "refrigerated": RefrigeratedStorage,
            "liquid": LiquidStorage,
        }

        container_type = action.get("container_type")
        weight = action.get("weight")

        if container_type in container_types and weight is not None:
            container_class = container_types[container_type]
            container = container_class(self.storage_counter, weight)
            self.storages[self.storage_counter] = container
            self.storage_counter += 1
        else:
            raise ValueError(f"Invalid container type '{container_type}' or missing weight.")

    def load_storage(self, action):
        vessel = self.vessels.get(action["vessel_id"])
        container = self.storages.get(action["container_id"])

        if vessel is None:
            raise ValueError(f"Vessel with ID {action['vessel_id']} does not exist.")
        if container is None:
            raise ValueError(f"Storage with ID {action['container_id']} does not exist.")

        if vessel.load_storage(container):
            vessel.current_harbor.containers.remove(container)

    def unload_storage(self, action):
        vessel = self.vessels.get(action["vessel_id"])
        container = self.storages.get(action["container_id"])

        if vessel is None:
            raise ValueError(f"Vessel with ID {action['vessel_id']} does not exist.")
        if container is None:
            raise ValueError(f"Storage with ID {action['container_id']} does not exist.")

        if vessel.unload_storage(container):
            vessel.current_harbor.containers.append(container)

    def navigate(self, action):
        vessel = self.vessels.get(action["vessel_id"])
        destination_harbor = self.harbors.get(action["destination_harbor"])

        if vessel is None:
            raise ValueError(f"Vessel with ID {action['vessel_id']} does not exist.")
        if destination_harbor is None:
            raise ValueError(f"Destination harbor with ID {action['destination_harbor']} does not exist.")

        vessel.navigate_to(destination_harbor)

    def refuel_vessel(self, action):
        vessel = self.vessels.get(action["vessel_id"])
        if vessel is None:
            raise ValueError(f"Vessel with ID {action['vessel_id']} does not exist.")

        vessel.refuel(action["amount"])

    def generate_json_output(self):
        output = {
            f"Harbor {harbor.harbor_id}": {
                "containers": [c.container_id for c in harbor.containers],
                "vessels": [vessel.vessel_id for vessel in harbor.active_ships]
            } for harbor in self.harbors.values()
        }
        with open('output.json', 'w') as f:
            json.dump(output, f, indent=4)

# Unit tests (updated)
class TestHarborManagementSystem(unittest.TestCase):
    def setUp(self):
        self.mock_vessel = Mock()
        self.mock_harbor = Harbor(1, 10.0, 20.0)
        self.mock_harbor.incoming_vessel(self.mock_vessel)

    def test_incoming_vessel(self):
        self.assertIn(self.mock_vessel, self.mock_harbor.active_ships)

    def test_outgoing_vessel(self):
        self.mock_harbor.outgoing_vessel(self.mock_vessel)
        self.assertNotIn(self.mock_vessel, self.mock_harbor.active_ships)
        self.assertIn(self.mock_vessel, self.mock_harbor.history)

    def test_product_creation(self):
        product = ProductFactory.create_product("small", 1, 10.0, 5, "C1")
        self.assertEqual(product.get_total_weight(), 50.0)

    def test_distance_calculation(self):
        harbor1 = Harbor(1, 10.0, 20.0)
        harbor2 = Harbor(2, 10.5, 21.0)
        self.assertAlmostEqual(harbor1.calculate_distance(harbor2), haversine(10.0, 20.0, 10.5, 21.0), places=2)

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
