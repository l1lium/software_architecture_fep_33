from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, id, weight, count, container_id):
        self._id = id
        self._weight = weight
        self._count = count
        self._container_id = container_id

    @abstractmethod
    def get_total_weight(self):
        return self._weight * self._count

class SmallItem(Item):
    def get_total_weight(self):
        return super().get_total_weight()

class HeavyItem(Item):
    def get_total_weight(self):
        return super().get_total_weight()

class RefrigeratedItem(Item):
    def get_total_weight(self):
        return super().get_total_weight()

class LiquidItem(Item):
    def get_total_weight(self):
        return super().get_total_weight()

class Ship(ABC):
    def __init__(self, id, fuel_capacity, container_capacity):
        self._id = id
        self._fuel_capacity = fuel_capacity
        self._container_capacity = container_capacity
        self._containers = []

    @abstractmethod
    def add_container(self, container):
        pass

class LightWeightShip(Ship):
    def add_container(self, container):
        if len(self._containers) < self._container_capacity:
            self._containers.append(container)
        else:
            print("Корабель не може прийняти більше контейнерів")

class MediumShip(Ship):
    def add_container(self, container):
        pass

class HeavyShip(Ship):
    def add_container(self, container):
        pass

class Port:
    def __init__(self, id, latitude, longitude):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._containers = []
        self._ships = []

    def add_ship(self, ship):
        self._ships.append(ship)

    def remove_ship(self, ship):
        self._ships.remove(ship)

    def add_container(self, container):
        self._containers.append(container)

    def remove_container(self, container):
        self._containers.remove(container)