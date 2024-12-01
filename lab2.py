from abc import ABC, abstractmethod
import math
import json

class IPort(ABC):
    @abstractmethod
    def incomingShip(self, ship):
        """Add ship to the current list"""
        pass

    @abstractmethod
    def outgoingShip(self, ship):
        """Add ship to the history list"""
        pass


class IShip(ABC):
    @abstractmethod
    def sailTo(self, port):
        """Return True if successfully sailed to the destination port"""
        pass

    @abstractmethod
    def refuel(self, new_fuel):
        """Add fuel to the ship"""
        pass

    @abstractmethod
    def load(self, container):
        """Return True if the container is successfully loaded"""
        pass

    @abstractmethod
    def unLoad(self, container):
        """Return True if the container is successfully unloaded"""
        pass


# Port Class
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
        # Haversine formula to calculate distance between two lat/long points
        R = 6371  # Radius of Earth in kilometers
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_port.latitude), math.radians(other_port.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance


# Ship Class
class Ship(IShip):
    def __init__(self, ID, fuel, current_port, total_weight_capacity, max_all_containers,
                 max_heavy_containers, max_refrigerated_containers, max_liquid_containers, fuel_per_km):
        self.ID = ID
        self.fuel = fuel
        self.current_port = current_port
        self.total_weight_capacity = total_weight_capacity
        self.max_all_containers = max_all_containers
        self.max_heavy_containers = max_heavy_containers
        self.max_refrigerated_containers = max_refrigerated_containers
        self.max_liquid_containers = max_liquid_containers
        self.fuel_per_km = fuel_per_km
        self.containers = []

    def sailTo(self, port):
        distance = self.current_port.getDistance(port)
        total_consumption = self.fuel_per_km * distance

        for container in self.containers:
            total_consumption += container.consumption() * distance

        if self.fuel >= total_consumption:
            self.fuel -= total_consumption
            self.current_port.outgoingShip(self)
            port.incomingShip(self)
            self.current_port = port
            return True
        else:
            return False

    def refuel(self, new_fuel):
        self.fuel += new_fuel

    def load(self, container):
        current_weight = sum(cont.weight for cont in self.containers)
        if current_weight + container.weight > self.total_weight_capacity:
            return False  # Exceeds weight capacity

        if len(self.containers) >= self.max_all_containers:
            return False  # Exceeds number of containers

        if isinstance(container, HeavyContainer) and len([cont for cont in self.containers if isinstance(cont, HeavyContainer)]) >= self.max_heavy_containers:
            return False  # Exceeds heavy container limit

        if isinstance(container, RefrigeratedContainer) and len([cont for cont in self.containers if isinstance(cont, RefrigeratedContainer)]) >= self.max_refrigerated_containers:
            return False  # Exceeds refrigerated container limit

        if isinstance(container, LiquidContainer) and len([cont for cont in self.containers if isinstance(cont, LiquidContainer)]) >= self.max_liquid_containers:
            return False  # Exceeds liquid container limit

        self.containers.append(container)
        return True

    def unLoad(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

    def getCurrentContainers(self):
        return sorted(self.containers, key=lambda x: x.ID)


# Abstract Container Class
class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

    def equals(self, other):
        return self.ID == other.ID and self.weight == other.weight


class BasicContainer(Container):
    def consumption(self):
        return self.weight * 2.50


class HeavyContainer(Container):
    def consumption(self):
        return self.weight * 3.00


class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return self.weight * 5.00


class LiquidContainer(HeavyContainer):
    def consumption(self):
        return self.weight * 4.00


# Main Class to parse input/output
class Main:
    def __init__(self):
        self.ports = {}
        self.ships = {}
        self.containers = {}
        self.container_counter = 0

    def run(self, input_file):
        with open(input_file, 'r') as file:
            data = json.load(file)

        print("Starting to process actions...")
        for action in data["actions"]:
            print(f"Processing action: {action}")  # Debug statement
            if action["type"] == "create_port":
                self.create_port(action)
            elif action["type"] == "create_ship":
                self.create_ship(action)
            elif action["type"] == "create_container":
                self.create_container(action)
            elif action["type"] == "load_container":
                self.load_container(action)
            elif action["type"] == "unload_container":
                self.unload_container(action)
            elif action["type"] == "sail":
                self.sail(action)
            elif action["type"] == "refuel":
                self.refuel_ship(action)

        self.generate_output()

    def create_port(self, action):
        port = Port(action["ID"], action["latitude"], action["longitude"])
        self.ports[action["ID"]] = port
        print(f"Created port {port.ID} at latitude {port.latitude} and longitude {port.longitude}.")

    def create_ship(self, action):
        port = self.ports[action["initial_port"]]
        ship = Ship(action["ID"], action["fuel"], port, action["total_weight_capacity"],
                    action["max_all_containers"], action["max_heavy_containers"],
                    action["max_refrigerated_containers"], action["max_liquid_containers"],
                    action["fuel_per_km"])
        port.incomingShip(ship)
        self.ships[action["ID"]] = ship
        print(f"Created ship {ship.ID} at port {port.ID} with fuel {ship.fuel}.")

    def create_container(self, action):
        # Ensure you are getting the correct container type
        container_type = action.get("container_type")
        if container_type == "basic":
            container = BasicContainer(self.container_counter, action["weight"])
        elif container_type == "heavy":
            container = HeavyContainer(self.container_counter, action["weight"])
        elif container_type == "refrigerated":
            container = RefrigeratedContainer(self.container_counter, action["weight"])
        elif container_type == "liquid":
            container = LiquidContainer(self.container_counter, action["weight"])
        else:
            print(f"Unknown container type: {container_type}")
            return

        # Add the container to the containers dictionary
        self.containers[self.container_counter] = container
        print(f"Created container {self.container_counter} of type {container_type} with weight {action['weight']}")

        if action["port"] in self.ports:
            port = self.ports[action["port"]]
            port.containers.append(container)
            print(f"Container {self.container_counter} added to port {action['port']}.")

        self.container_counter += 1

    def load_container(self, action):
        print(f"Attempting to load container {action['container_id']} onto ship {action['ship_id']}")
        ship = self.ships[action["ship_id"]]
        if action["container_id"] in self.containers:
            container = self.containers[action["container_id"]]
            port = ship.current_port
            if container in port.containers and ship.load(container):
                port.containers.remove(container)
                print(f"Loaded container {action['container_id']} onto ship {action['ship_id']}.")
            else:
                print(f"Container {action['container_id']} is not in the port or cannot be loaded.")
        else:
            print(f"Container {action['container_id']} does not exist.")

    def unload_container(self, action):
        ship = self.ships[action["ship_id"]]
        container = self.containers[action["container_id"]]
        if ship.unLoad(container):
            ship.current_port.containers.append(container)
            print(f"Unloaded container {action['container_id']} from ship {action['ship_id']}.")
        else:
            print(f"Could not unload container {action['container_id']} from ship {action['ship_id']}.")

    def sail(self, action):
        ship = self.ships[action["ship_id"]]
        destination_port = self.ports[action["destination_port"]]
        if ship.sailTo(destination_port):
            print(f"Sailed from {ship.current_port.ID} to {destination_port.ID}.")
        else:
            print(f"Failed to sail from {ship.current_port.ID} to {destination_port.ID}. Not enough fuel.")

    def refuel_ship(self, action):
        ship = self.ships[action["ship_id"]]
        ship.refuel(action["amount"])
        print(f"Refueled ship {action['ship_id']} by {action['amount']}.")

    def generate_output(self):
        output = {}
        for port in self.ports.values():
            output[f"Port {port.ID}"] = {
                "lat": port.latitude,
                "lon": port.longitude,
                "basic_container": [c.ID for c in port.containers if isinstance(c, BasicContainer)],
                "heavy_container": [c.ID for c in port.containers if isinstance(c, HeavyContainer) and not isinstance(c, RefrigeratedContainer) and not isinstance(c, LiquidContainer)],
                "refrigerated_container": [c.ID for c in port.containers if isinstance(c, RefrigeratedContainer)],
                "liquid_container": [c.ID for c in port.containers if isinstance(c, LiquidContainer)],
                "ships": {
                    f"ship_{ship.ID}": {
                        "fuel_left": round(ship.fuel, 2),
                        "basic_container": [c.ID for c in ship.containers if isinstance(c, BasicContainer)],
                        "heavy_container": [c.ID for c in ship.containers if isinstance(c, HeavyContainer) and not isinstance(c, RefrigeratedContainer) and not isinstance(c, LiquidContainer)],
                        "refrigerated_container": [c.ID for c in ship.containers if isinstance(c, RefrigeratedContainer)],
                        "liquid_container": [c.ID for c in ship.containers if isinstance(c, LiquidContainer)],
                    } for ship in port.current
                }
            }

        with open('output.json', 'w') as outfile:
            json.dump(output, outfile, indent=4)

if __name__ == "__main__":
    main = Main()
    main.run('input_file.json')  # Make sure to have your input JSON file named correctly
