import json
from math import sqrt

# Base Container class
class Container:
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    def consumption(self):
        raise NotImplementedError("This method must be implemented in subclasses")

    def __eq__(self, other):
        return isinstance(other, Container) and self.ID == other.ID and self.weight == other.weight


# Specialized containers
class BasicContainer(Container):
    def consumption(self):
        return 2.5 * self.weight


class HeavyContainer(Container):
    def consumption(self):
        return 3.0 * self.weight


class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return 5.0 * self.weight


class LiquidContainer(HeavyContainer):
    def consumption(self):
        return 4.0 * self.weight


# Port class
class Port:
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
        if ship not in self.history:
            self.history.append(ship)

    def outgoingShip(self, ship):
        if ship in self.current:
            self.current.remove(ship)

    def getDistance(self, other):
        return sqrt((self.latitude - other.latitude) ** 2 + (self.longitude - other.longitude) ** 2)


# Ship class
class Ship:
    def __init__(self, ID, fuel, currentPort, totalWeightCapacity, maxContainers, maxHeavy, maxRefrigerated, maxLiquid, fuelConsumptionPerKM):
        self.ID = ID
        self.fuel = fuel
        self.currentPort = currentPort
        self.totalWeightCapacity = totalWeightCapacity
        self.maxContainers = maxContainers
        self.maxHeavy = maxHeavy
        self.maxRefrigerated = maxRefrigerated
        self.maxLiquid = maxLiquid
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.containers = []

    def sailTo(self, port):
        distance = self.currentPort.getDistance(port)
        fuelNeeded = distance * self.fuelConsumptionPerKM + sum(container.consumption() for container in self.containers)
        if self.fuel >= fuelNeeded:
            self.fuel -= fuelNeeded
            self.currentPort.outgoingShip(self)
            self.currentPort = port
            port.incomingShip(self)
            return True
        return False

    def reFuel(self, amount):
        self.fuel += amount

    def load(self, container):
        if (
            len(self.containers) < self.maxContainers and
            sum(c.weight for c in self.containers) + container.weight <= self.totalWeightCapacity and
            (
                (isinstance(container, HeavyContainer) and len([c for c in self.containers if isinstance(c, HeavyContainer)]) < self.maxHeavy) or
                (isinstance(container, RefrigeratedContainer) and len([c for c in self.containers if isinstance(c, RefrigeratedContainer)]) < self.maxRefrigerated) or
                (isinstance(container, LiquidContainer) and len([c for c in self.containers if isinstance(c, LiquidContainer)]) < self.maxLiquid)
            )
        ):
            self.containers.append(container)
            return True
        return False

    def unLoad(self, container):
        if container in self.containers:
            self.containers.remove(container)
            self.currentPort.containers.append(container)
            return True
        return False


# Main handler
class Main:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.ports = {}
        self.ships = {}
        self.containers = {}

    def run(self):
        with open(self.input_file, 'r') as file:
            data = json.load(file)
        self.processCommands(data)
        self.writeOutput()

    def processCommands(self, commands):
        for command in commands:
            action = command['action']
            if action == "create_port":
                self.createPort(command)
            elif action == "create_ship":
                self.createShip(command)
            elif action == "create_container":
                self.createContainer(command)
            elif action == "load_container":
                self.loadContainer(command)
            elif action == "unload_container":
                self.unloadContainer(command)
            elif action == "sail":
                self.sailShip(command)
            elif action == "refuel":
                self.refuelShip(command)

    def createPort(self, command):
        port = Port(command['ID'], command['latitude'], command['longitude'])
        self.ports[port.ID] = port

    def createShip(self, command):
        port = self.ports[command['currentPort']]
        ship = Ship(
            command['ID'], command['fuel'], port,
            command['totalWeightCapacity'], command['maxContainers'],
            command['maxHeavy'], command['maxRefrigerated'], command['maxLiquid'],
            command['fuelConsumptionPerKM']
        )
        port.incomingShip(ship)
        self.ships[ship.ID] = ship

    def createContainer(self, command):
        if command['type'] == "Basic":
            container = BasicContainer(command['ID'], command['weight'])
        elif command['type'] == "Refrigerated":
            container = RefrigeratedContainer(command['ID'], command['weight'])
        elif command['type'] == "Liquid":
            container = LiquidContainer(command['ID'], command['weight'])
        else:
            container = HeavyContainer(command['ID'], command['weight'])
        self.containers[container.ID] = container

    def loadContainer(self, command):
        ship = self.ships[command['shipID']]
        container = self.containers[command['containerID']]
        if container in ship.currentPort.containers:
            if ship.load(container):
                ship.currentPort.containers.remove(container)

    def unloadContainer(self, command):
        ship = self.ships[command['shipID']]
        container = self.containers[command['containerID']]
        if ship.unLoad(container):
            ship.currentPort.containers.append(container)

    def sailShip(self, command):
        ship = self.ships[command['shipID']]
        destination = self.ports[command['destinationPort']]
        ship.sailTo(destination)

    def refuelShip(self, command):
        ship = self.ships[command['shipID']]
        ship.reFuel(command['amount'])

    def writeOutput(self):
        output = {}
        for port in sorted(self.ports.values(), key=lambda p: p.ID):
            port_data = {
                "lat": round(port.latitude, 2),
                "lon": round(port.longitude, 2),
                "containers": [c.ID for c in port.containers],
                "ships": {
                    ship.ID: round(ship.fuel, 2) for ship in port.current
                }
            }
            output[f"Port {port.ID}"] = port_data
        with open(self.output_file, 'w') as file:
            json.dump(output, file, indent=4)


