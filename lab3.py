from abc import ABC, abstractmethod
from typing import List, Dict
from dataclasses import dataclass

# Abstract Item Class
class Item(ABC):
    def __init__(self, item_id: int, weight: float, count: int, container_id: int):
        self.item_id = item_id
        self.weight = weight
        self.count = count
        self.container_id = container_id

    @abstractmethod
    def get_total_weight(self) -> float:
        pass

@dataclass
class SmallItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count

@dataclass
class HeavyItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count * 1.5  # Extra factor for heavy items

@dataclass
class RefrigeratedItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count * 1.2  # Factor for refrigerated items

@dataclass
class LiquidItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count * 1.1  # Factor for liquid items

# Factory for Items
class ItemFactory:
    @staticmethod
    def create_item(item_type: str, item_id: int, weight: float, count: int, container_id: int) -> Item:
        if item_type == "Small":
            return SmallItem(item_id, weight, count, container_id)
        elif item_type == "Heavy":
            return HeavyItem(item_id, weight, count, container_id)
        elif item_type == "Refrigerated":
            return RefrigeratedItem(item_id, weight, count, container_id)
        elif item_type == "Liquid":
            return LiquidItem(item_id, weight, count, container_id)
        else:
            raise ValueError(f"Unknown item type: {item_type}")

# Abstract Ship Class
class Ship(ABC):
    def __init__(self, ship_id: int, max_weight: float, fuel_capacity: float):
        self.ship_id = ship_id
        self.max_weight = max_weight
        self.fuel_capacity = fuel_capacity
        self.containers: List[Item] = []

    @abstractmethod
    def add_container(self, item: Item):
        pass

    def get_total_weight(self) -> float:
        return sum(container.get_total_weight() for container in self.containers)

@dataclass
class LightWeightShip(Ship):
    def add_container(self, item: Item):
        if self.get_total_weight() + item.get_total_weight() > self.max_weight:
            raise ValueError("Exceeds maximum weight for LightWeightShip.")
        self.containers.append(item)

@dataclass
class MediumShip(Ship):
    def add_container(self, item: Item):
        if self.get_total_weight() + item.get_total_weight() > self.max_weight:
            raise ValueError("Exceeds maximum weight for MediumShip.")
        self.containers.append(item)

@dataclass
class HeavyShip(Ship):
    def add_container(self, item: Item):
        if self.get_total_weight() + item.get_total_weight() > self.max_weight:
            raise ValueError("Exceeds maximum weight for HeavyShip.")
        self.containers.append(item)

# Builder for Ships
class ShipBuilder:
    def __init__(self):
        self._ship = None

    def create_lightweight_ship(self, ship_id: int, max_weight: float, fuel_capacity: float):
        self._ship = LightWeightShip(ship_id, max_weight, fuel_capacity)

    def create_medium_ship(self, ship_id: int, max_weight: float, fuel_capacity: float):
        self._ship = MediumShip(ship_id, max_weight, fuel_capacity)

    def create_heavy_ship(self, ship_id: int, max_weight: float, fuel_capacity: float):
        self._ship = HeavyShip(ship_id, max_weight, fuel_capacity)

    def get_ship(self) -> Ship:
        return self._ship

# Example Usage
if __name__ == "__main__":
    # Create Items using Factory
    item1 = ItemFactory.create_item("Small", 1, 10.0, 5, 1001)
    item2 = ItemFactory.create_item("Heavy", 2, 50.0, 2, 1002)

    # Build Ships using Builder
    builder = ShipBuilder()
    builder.create_medium_ship(1, 500.0, 100.0)
    ship = builder.get_ship()

    # Add Items to Ship
    ship.add_container(item1)
    ship.add_container(item2)

    # Output Ship Details
    print(f"Ship ID: {ship.ship_id}, Total Weight: {ship.get_total_weight()} kg")
