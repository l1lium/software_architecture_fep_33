import json
from abc import ABC, abstractmethod
from typing import List

class IPort(ABC):
    @abstractmethod
    def incomingShip(self, ship):
        pass

    @abstractmethod
    def outgoingShip(self, ship):
        pass

class IShip(ABC):
    @abstractmethod
    def sailTo(self, port):
        pass

    @abstractmethod
    def reFuel(self, newFuel):
        pass

    @abstractmethod
    def load(self, container):
        pass

    @abstractmethod
    def unLoad(self, container):
        pass

class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        return self.ID == other.ID and self.weight == other.weight

class BasicContainer(Container):
    def __init__(self, ID, weight):
        super().__init__(ID, weight)

    def consumption(self):
        return 2.50 * self.weight

    def __eq__(self, other):
        return isinstance(other, BasicContainer) and super().__eq__(other)

class HeavyContainer(Container):
    def __init__(self, ID, weight):
        super().__init__(ID, weight)

    def consumption(self):
        return 3.00 * self.weight

    def __eq__(self, other):
        return isinstance(other, HeavyContainer) and super().__eq__(other)

class RefrigeratedContainer(HeavyContainer):
    def __init__(self, ID, weight):
        super().__init__(ID, weight)

    def consumption(self):
        return 5.00 * self.weight

    def __eq__(self, other):
        return isinstance(other, RefrigeratedContainer) and super().__eq__(other)

class LiquidContainer(HeavyContainer):
    def __init__(self, ID, weight):
        super().__init__(ID, weight)

    def consumption(self):
        return 4.00 * self.weight

    def __eq__(self, other):
        return isinstance(other, LiquidContainer) and super().__eq__(other)

class Port(IPort):
    def __init__(self, ID, latitude, longitude):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []  
        self.history = []  
        self.current = []  

    def incomingShip(self, ship):
        if ship not in self.current:
            self.current.append(ship)

    def outgoingShip(self, ship):
        if ship not in self.history:
            self.history.append(ship)
            if ship in self.current:
                self.current.remove(ship)

    def getDistance(self, other_port):
        pass

class Ship(IShip):
    def __init__(self, ID, fuel, port, totalWeightCapacity, maxNumContainers, maxHeavyContainers, maxRefrigeratedContainers, maxLiquidContainers, fuelConsumptionPerKM):
        self.ID = ID
        self.fuel = fuel
        self.currentPort = port
        self.totalWeightCapacity = totalWeightCapacity
        self.maxNumContainers = maxNumContainers
        self.maxHeavyContainers = maxHeavyContainers
        self.maxRefrigeratedContainers = maxRefrigeratedContainers
        self.maxLiquidContainers = maxLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.containers = []

    def sailTo(self, port):
        if self.fuel > 0:
            self.currentPort.outgoingShip(self)
            self.currentPort = port
            port.incomingShip(self)
            return True
        return False

    def reFuel(self, newFuel):
        self.fuel += newFuel

    def load(self, container):
        if len(self.containers) < self.maxNumContainers:
            self.containers.append(container)
            return True
        return False

    def unLoad(self, container):
        if container in self.containers:
            self.containers.remove(container)
            self.currentPort.containers.append(container)
            return True
        return False

    def getCurrentContainers(self):
        return sorted(self.containers, key=lambda x: x.ID)