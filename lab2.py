from abc import ABC, abstractmethod
import math
import json

class PortInterface(ABC):
    @abstractmethod
    def add_incoming_ship(self, ship):
        """Add the ship to the current port's list of ships"""
        pass

    @abstractmethod
    def add_outgoing_ship(self, ship):
        """Add the ship to the history of ships that have left the port"""
        pass


class ShipInterface(ABC):
    @abstractmethod
    def sail_to_port(self, port):
        """Return True if the ship successfully sails to the target port"""
        pass

    @abstractmethod
    def refuel(self, fuel_amount):
        """Refuel the ship with the specified amount of fuel"""
        pass

    @abstractmethod
    def load_container(self, container):
        """Return True if the container is successfully loaded onto the ship"""
        pass

    @abstractmethod
    def unload_container(self, container):
        """Return True if the container is successfully unloaded from the ship"""
        pass


# Port Class
class Port(PortInterface):
    def __init__(self, port_id, latitude, longitude):
        self.port_id = port_id
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current_ships = []

    def add_incoming_ship(self, ship):
        if ship not in self.current_ships:
            self.current_ships.append(ship)

    def add_outgoing_ship(self, ship):
        if ship not in self.history:
            self.history.append(ship)
        if ship in self.current_ships:
            self.current_ships.remove(ship)

    def calculate_distance(self, other_port):
        # Haversine formula for calculating distance between two lat/long points
        R = 6371  # Earth radius in kilometers
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_port.latitude), math.radians(other_port.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance


# Ship Class
class Ship(ShipInterface):
    def __init__(self, ship_id, fuel, current_port, weight_capacity, max_containers, max_heavy, max_refrigerated, max_liquid, fuel_per_km):
        self.ship_id = ship_id
        self.fuel = fuel
        self.current_port = current_port
        self.weight_capacity = weight_capacity
        self.max_containers = max_containers
        self.max_heavy_containers = max_heavy
        self.max_refrigerated_containers = max_refrigerated
        self.max_liquid_containers = max_liquid
        self.fuel_per_km = fuel_per_km
        self.containers = []

    def sail_to_port(self, port):
        distance = self.current_port.calculate_distance(port)
        total_fuel_needed = self.fuel_per_km * distance

        for container in self.containers:
            total_fuel_needed += container.calculate_consumption() * distance

        if self.fuel >= total_fuel_needed:
            self.fuel -= total_fuel_needed
            self.current_port.add_outgoing_ship(self)
            port.add_incoming_ship(self)
            self.current_port = port
            return True
        return False

    def refuel(self, fuel_amount):
        self.fuel += fuel_amount

    def load_container(self, container):
        current_weight = sum(cont.weight for cont in self.containers)
        if current_weight + container.weight > self.weight_capacity:
            return False  # Exceeds weight capacity

        if len(self.containers) >= self.max_containers:
            return False  # Exceeds container limit

        if isinstance(container, HeavyContainer) and len([cont for cont in self.containers if isinstance(cont, HeavyContainer)]) >= self.max_heavy_containers:
            return False  # Exceeds heavy container limit

        if isinstance(container, RefrigeratedContainer) and len([cont for cont in self.containers if isinstance(cont, RefrigeratedContainer)]) >= self.max_refrigerated_containers:
            return False  # Exceeds refrigerated container limit

        if isinstance(container, LiquidContainer) and len([cont for cont in self.containers if isinstance(cont, LiquidContainer)]) >= self.max_liquid_containers:
            return False  # Exceeds liquid container limit

        self.containers.append(container)
        return True

    def unload_container(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

    def get_current_containers(self):
        return sorted(self.containers, key=lambda x: x.container_id)


# Abstract Container Class
class Container(ABC):
    def __init__(self, container_id, weight):
        self.container_id = container_id
        self.weight = weight

    @abstractmethod
    def calculate_consumption(self):
        pass

    def equals(self, other):
        return self.container_id == other.container_id and self.weight == other.weight


class BasicContainer(Container):
    def calculate_consumption(self):
        return self.weight * 2.50


class HeavyContainer(Container):
    def calculate_consumption(self):
        return self.weight * 3.00


class RefrigeratedContainer(HeavyContainer):
    def calculate_consumption(self):
        return self.weight * 5.00


class LiquidContainer(HeavyContainer):
    def calculate_consumption(self):
        return self.weight * 4.00


# Main Class to process input/output
class PortOperation:
    def __init__(self):
        self.ports = {}
        self.ships = {}
        self.containers = {}
        self.container_counter = 0

    def execute(self, input_file):
        with open(input_file, 'r') as file:
            data = json.load(file)

        print("Processing actions...")
        for action in data["actions"]:
            print(f"Processing: {action}")  # Debugging statement
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
        print(f"Created port {port.port_id} at latitude {port.latitude}, longitude {port.longitude}.")

    def create_ship(self, action):
        port = self.ports[action["initial_port"]]
        ship = Ship(action["ID"], action["fuel"], port, action["total_weight_capacity"],
                    action["max_all_containers"], action["max_heavy_containers"],
                    action["max_refrigerated_containers"], action["max_liquid_containers"],
                    action["fuel_per_km"])
        port.add_incoming_ship(ship)
        self.ships[action["ID"]] = ship
        print(f"Created ship {ship.ship_id} at port {port.port_id} with fuel {ship.fuel}.")

    def create_container(self, action):
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

        self.containers[self.container_counter] = container
        print(f"Created container {self.container_counter} of type {container_type} with weight {action['weight']}")

        if action["port"] in self.ports:
            port = self.ports[action["port"]]
            port.containers.append(container)
            print(f"Added container {self.container_counter} to port {action['port']}.")

        self.container_counter += 1

    def load_container(self, action):
        print(f"Loading container {action['container_id']} onto ship {action['ship_id']}")
        ship = self.ships[action["ship_id"]]
        if action["container_id"] in self.containers:
            container = self.containers[action["container_id"]]
            port = ship.current_port
            if container in port.containers and ship.load_container(container):
                port.containers.remove(container)
                print(f"Loaded container {action['container_id']} onto ship {action['ship_id']}.")
            else:
                print(f"Container {action['container_id']} is not in the port or cannot be loaded.")
        else:
            print(f"Container {action['container_id']} does not exist.")

    def unload_container(self, action):
        ship = self.ships[action["ship_id"]]
        container = self.containers[action["container_id"]]
        if ship.unload_container(container):
            ship.current_port.containers.append(container)
            print(f"Unloaded container {action['container_id']} from ship {action['ship_id']}.")
        else:
            print(f"Could not unload container {action['container_id']} from ship {action['ship_id']}.")

    def sail(self, action):
        ship = self.ships[action["ship_id"]]
        destination_port = self.ports[action["destination_port"]]
        if ship.sail_to_port(destination_port):
            print(f"Sailed from {ship.current_port.port_id} to {destination_port.port_id}.")
        else:
            print(f"Failed to sail from {ship.current_port.port_id} to {destination_port.port_id}. Not enough fuel.")

    def refuel_ship(self, action):
        ship = self.ships[action["ship_id"]]
        ship.refuel(action["amount"])
        print(f"Refueled ship {action['ship_id']} by {action['amount']}.")

    def generate_output(self):
        output = {}
        for port in self.ports.values():
            output[f"Port {port.port_id}"] = {
                "lat": port.latitude,
                "lon": port.longitude,
                "basic_container": [c.container_id for c in port.containers if isinstance(c, BasicContainer)],
                "heavy_container": [c.container_id for c in port.containers if isinstance(c, HeavyContainer) and not isinstance(c, RefrigeratedContainer) and not isinstance(c, LiquidContainer)],
                "refrigerated_container": [c.container_id for c in port.containers if isinstance(c, RefrigeratedContainer)],
                "liquid_container": [c.container_id for c in port.containers if isinstance(c, LiquidContainer)],
                "ships": {
                    f"ship_{ship.ship_id}": {
                        "fuel_left": round(ship.fuel, 2),
                        "basic_container": [c.container_id for c in ship.containers if isinstance(c, BasicContainer)],
                        "heavy_container": [c.container_id for c in ship.containers if isinstance(c, HeavyContainer) and not isinstance(c, RefrigeratedContainer) and not isinstance(c, LiquidContainer)],
                        "refrigerated_container": [c.container_id for c in ship.containers if isinstance(c, RefrigeratedContainer)],
                        "liquid_container": [c.container_id for c in ship.containers if isinstance(c, LiquidContainer)],
                    } for ship in port.current_ships
                }
            }

        with open('output.json', 'w') as outfile:
            json.dump(output, outfile, indent=4)

if __name__ == "__main__":
    port_operation = PortOperation()
    port_operation.execute('input_file.json')  # Ensure your input JSON file is named correctly
