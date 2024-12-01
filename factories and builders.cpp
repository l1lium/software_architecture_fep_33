#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <stdexcept>
#include <cmath>
#include <memory>


#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

using namespace std;

const double EARTH_RADIUS_KM = 6371.0;

inline double Radian(double angle)
{
	return M_PI * angle / 180.0;
}

class Container;
class Ship;
class Port;

class Iport { // I == Interface
public:

	//	virtual void OnlyVirtual();

	virtual double getDistance(const Iport& other) const = 0;

	virtual void incomingShip(class Ship* s) = 0;

	virtual void outgoingShip(class Ship* s) = 0;

	virtual int getID() const = 0;

	virtual ~Iport() {};
};

class Iship { // I == interface
public:
	//	virtual void OnlyVirtual();

	virtual vector<unique_ptr<Container>>& GetCurrentContainers() = 0;

	virtual bool sailTo(Port* p) = 0;

	virtual void reFuel(double newFuel) = 0;

	virtual bool load(unique_ptr<Container> count) = 0;

	virtual bool unload(Port& port, unique_ptr<Container> cont) = 0;

	virtual ~Iship() {}
};



class Container {
protected:
	int ID;
	int weight;

	Container(int ID, int weight) : ID(ID), weight(weight) {}
public:
	virtual ~Container() {}

	bool equals(const Container& other) const {
		return (typeid(*this) == typeid(other)) && (this->weight == other.weight);
	};

	int getID() const {
		return ID;
	}
	int getWeight() const {
		return weight;
	}
	virtual double getFuelConsumption() const = 0;

};

class BasicContainer : public Container {
public:
	BasicContainer(int ID, int weight) : Container(ID, weight) {
		if (weight > 3000) {
			throw invalid_argument("Weight of a BasicContainer must be <= 3000");
		}
	}
	double getFuelConsumption() const override {
		return weight * 2.50;
	}
};

class HeavyContainer : public Container {
public:
	HeavyContainer(int ID, int weight) : Container(ID, weight) {
		if (weight <= 3000) {
			throw invalid_argument("Weight of a HeavyContainer must be > 3000");
		}
	}
	double getFuelConsumption() const override {
		return weight * 3.00;
	}


};

class RefrigeratedContainer : public HeavyContainer {
public:
	RefrigeratedContainer(int ID, int weight) : HeavyContainer(ID, weight) {}

	double getFuelConsumption() const override {
		return weight * 5.00;
	}

};

class LiquidContainer : public HeavyContainer {
public:
	LiquidContainer(int ID, int weight) : HeavyContainer(ID, weight) {}

	double getFuelConsumption() const override {
		return weight * 4.00;
	}
};



class Port : public Iport {
public:
	//	virtual void OnlyVirtual() override {};	 // interface realisation
	int ID;
	double latitude;
	double longitude;
	vector<unique_ptr<Container>> Containers;
	vector<class Ship*> current;
	vector<class Ship*> history;

	Port(int ID, double lat, double lon)
		: ID(ID), latitude(lat), longitude(lon) {}

	int getID() const  override {
		return ID;
	}

	double getDistance(const Iport& otherPort) const override {

		const Port& other = dynamic_cast<const Port&>(otherPort);

		double lat1 = Radian(this->latitude);
		double log1 = Radian(this->longitude);
		double lat2 = Radian(other.latitude);
		double log2 = Radian(other.longitude);

		double difflat = lat2 - lat1;
		double difflog = log2 - log1;

		double computation = 2 * asin(sqrt(sin(difflat / 2) * sin(difflat / 2) + cos(lat1) * cos(lat2) * sin(difflog / 2) * sin(difflog / 2)));
		return EARTH_RADIUS_KM * computation;
	};
	void incomingShip(Ship* s) override {
		current.push_back(s);
	}
	void outgoingShip(Ship* s) override {
		auto it = find(current.begin(), current.end(), s); // Find ship in current list
		if (it != current.end()) {
			current.erase(it); // Remove from current
			history.push_back(s); // Add to history
		}
	}
};

class CapacityLimits { // CapacityLimits class to group capacity-related variables
public:

	int totalWeightCapacity;
	int maxNumberOfAllContainers;
	int maxNumberOfHeavyContainers;
	int maxNumberOfRefrigeratedContainers;
	int maxNumberOfLiquidContainers;

	CapacityLimits(int totalWeight, int allContainers, int heavyContainers, int refrigeratedContainers, int liquidContainers)
		: totalWeightCapacity(totalWeight), maxNumberOfAllContainers(allContainers), maxNumberOfHeavyContainers(heavyContainers), maxNumberOfRefrigeratedContainers(refrigeratedContainers),
		maxNumberOfLiquidContainers(liquidContainers) {};

};

class Ship : public Iship {
public:
	//	virtual void OnlyVirtual() override {};    // interface realisation
	int ID;
	double Fuel;
	Iport* currentPort;
	CapacityLimits capacityLimit;
	double fuelConsumptionPerKM;
	vector<unique_ptr<Container>> currentContainers;

	Ship(int id, double fuel, Iport* currentPort, CapacityLimits capacityLimit, double fuelConsumptionPerKM)
		: ID(id), Fuel(fuel), currentPort(currentPort), capacityLimit(capacityLimit), fuelConsumptionPerKM(fuelConsumptionPerKM) {}

	int getID() const {
		return ID;
	}

	Iport* getCurrentPort() const {
		return currentPort;
	}

	bool sailTo(Port* destinationPort) override {
		// Check if the ship is already at the target port
		if (currentPort == destinationPort) {
			return false; // Already at the destination
		}
		double distance = currentPort->getDistance(*destinationPort);
		double fuelNeeded = fuelConsumptionPerKM * distance;

		for (const auto& container : currentContainers) {
			fuelNeeded += container->getFuelConsumption();
		}

		// Check if there is enough fuel to sail
		if (Fuel < fuelNeeded) {
			cout << "Not enough fuel to sail to the destination port." << endl;
			return false; // Not enough fuel to sail
		}

		// Update fuel and move the ship
		Fuel -= fuelNeeded; // Deduct the fuel used
		currentPort->outgoingShip(this); // Notify the current port
		currentPort = destinationPort; // Update the current port
		currentPort->incomingShip(this); // Notify the new port

		cout << "Fuel was used: " << Fuel << " units." << endl;
		return true; // Successfully sailed to the destination
	}

	void reFuel(double newFuel) override {
		Fuel += newFuel; // Add fuel to the ship
	}

	bool load(unique_ptr<Container> cont) override {
		// Check capacity limit before loading
		if (currentContainers.size() >= capacityLimit.maxNumberOfAllContainers) {
			throw runtime_error("Ship is at full container capacity");
		}

		int totalWeight = 0;
		for (const auto& c : currentContainers) {
			totalWeight += c->getWeight();
		}
		totalWeight += cont->getWeight();

		if (totalWeight > capacityLimit.totalWeightCapacity) {
			cout << "Ship exceeded weight capacity" << endl;
			return false;
		}

		cout << "Loading container with ID: " << cont->getID() << " and weight: " << cont->getWeight() << endl;
		currentContainers.push_back(move(cont));  // Move ownership of container
		return true;
	}

	bool unload(Port& port, unique_ptr<Container> cont) override {
		auto it = find_if(currentContainers.begin(), currentContainers.end(),
			[&](const unique_ptr<Container>& c) { return c->getID() == cont->getID(); });

		if (it != currentContainers.end()) {
			port.Containers.push_back(move(*it)); // Move the container to the port's storage
			currentContainers.erase(it); // Remove the container from the ship
			return true; // Successfully unloaded
		}
		return false; // Container not found
	}

	vector<unique_ptr<Container>>& GetCurrentContainers() override {
		return currentContainers;
	};

};

class LightWeightShip : public Ship {
public:
	LightWeightShip(int id, double fuel, Iport* port, CapacityLimits capacityLimit, double fuelConsumption)
		: Ship(id, fuel, port, capacityLimit, fuelConsumption) {}
};
class MediumWeightShip : public Ship {
public:
	MediumWeightShip(int id, double fuel, Iport* port, CapacityLimits capacityLimit, double fuelConsumption)
		: Ship(id, fuel, port, capacityLimit, fuelConsumption) {}
};
class HeavyWeightShip : public Ship {
public:
	HeavyWeightShip(int id, double fuel, Iport* port, CapacityLimits capacityLimit, double fuelConsumption)
		: Ship(id, fuel, port, capacityLimit, fuelConsumption) {}
};

class ShipFactory {
public:
 	virtual ~ShipFactory() {}
 	virtual unique_ptr<Ship> createShip(int id, Iport* port, double initialFuel) = 0;
};

class LightWeightShipFactory : public ShipFactory {
public:
	unique_ptr<Ship> createShip(int id, Iport* port, double initialFuel) override {
		CapacityLimits capacity(7500, 5, 0, 0, 0);  // LightWeightShip specifics
		return make_unique<LightWeightShip>(id, initialFuel, port, capacity, 0.5);
	}
};
class MediumWeightShipFactory : public ShipFactory {
public:
	unique_ptr<Ship> createShip(int id, Iport* port, double initialFuel) override {
		CapacityLimits capacity(15000, 5, 2, 1, 1);  // LightWeightShip specifics
		return make_unique<MediumWeightShip>(id, initialFuel, port, capacity, 1.2);
	}
};
class HeavyWeightShipFactory : public ShipFactory {
public:
	unique_ptr<Ship> createShip(int id, Iport* port, double initialFuel) override {
		CapacityLimits capacity(50000, 5, 5, 5, 5);  // LightWeightShip specifics
		return make_unique<HeavyWeightShip>(id, initialFuel, port, capacity, 2.0);
	}
};




class ShipBuilder {
public:

	virtual void setID(int id) = 0;
	virtual void setFuelBank(double fuelCapacity) = 0;
	virtual void setCapacityLimits(const CapacityLimits& limits) = 0;
	virtual unique_ptr<Ship> getResult() = 0;

	virtual ~ShipBuilder() {}
};

class  LightWeightShipBuilder : public ShipBuilder {
	unique_ptr<LightWeightShip> ship;
public:

	LightWeightShipBuilder(int id, double fuel, Iport* port)
		: ship(make_unique<LightWeightShip>(id, fuel, port, CapacityLimits(7500, 5, 0, 0, 0), 0.5)) {}

	void setID(int id) override { ship->ID = id; }
	void setFuelBank(double fuelCapacity) override { ship->Fuel += fuelCapacity; }
	void setCapacityLimits(const CapacityLimits& limits) override { ship->capacityLimit = limits; }
	unique_ptr<Ship> getResult() override { return move(ship); }
};

class MediumWeightShipBuilder : public ShipBuilder {
	unique_ptr<MediumWeightShip> ship;
public:

	MediumWeightShipBuilder(int id, double fuel, Iport* port)
		: ship(make_unique<MediumWeightShip>(id, fuel, port, CapacityLimits(15000, 5, 2, 1, 1), 1.2)) {}

	void setID(int id) override { ship->ID = id; }
	void setFuelBank(double fuelCapacity) override { ship->Fuel += fuelCapacity; }
	void setCapacityLimits(const CapacityLimits& limits) override { ship->capacityLimit = limits; }
	unique_ptr<Ship> getResult() override { return move(ship); }
};




class Main {
public:
	static void printCurrentContainers(Ship& ship) {
		// Get the current containers from the ship
		const auto& containers = ship.GetCurrentContainers();
		cout << "List of containers from ship ID: " << ship.getID() << endl;
		if (containers.empty()) {
			cout << "there is no containers" << endl;  // Message for empty container list
			return;
		}
		// Print the details of each container

		for (const auto& container : containers) {
			cout << "Container ID: " << container->getID()
				<< ", Weight: " << container->getWeight() << endl;
		}
	}

	static void sailToPort(Ship& ship, Port& destinationPort) {
		if (ship.sailTo(&destinationPort)) {
			// If the sailing was successful, display the containers
			cout << "Successfully sailed to port ID: " << destinationPort.getID() << endl;
		}
	}

	static void displayContainersAtCurrentPort(const Port& port) {
		cout << "Containers at Port ID: " << port.getID() << endl;

		if (port.Containers.empty()) { // Assuming 'Containers' is a member of the Port class
			cout << "No containers at this port." << endl;
		}
		else {
			for (const auto& container : port.Containers) {
				cout << "Container ID: " << container->getID()
					<< ", Weight: " << container->getWeight() << endl;
			}
		}
	}


};



class Item {
protected:
	int ID;
	double weight;
	int count;
	int containerID;

public:

	Item(int ID, double  weight, int  coun, int containerID) : ID(ID), weight(weight), count(coun), containerID(containerID) {}

	virtual ~Item() {}

	virtual double getTotalWeight() const { 
		return weight * count; 
	}
	int getID() const {
		return ID; 
	}
	int getContainerID() const { 
		return containerID; 
	}

	virtual string getType() const = 0;

};
class SmallItem : public Item {
public:
	SmallItem(int id, double weight, int count, int containerId) : Item(id, weight, count, containerId) {}
	double getTotalWeight() const override { return weight * count; }

	string getType() const override { 
		return "Small";
	}
};
class HeavyItem : public Item {
public:
	HeavyItem(int id, double weight, int count, int containerId) : Item(id, weight, count, containerId) {}
	double getTotalWeight() const override { return weight * count; }

	string getType() const override { 
		return "Heavy"; 
	}
};
class RefrigeratedItem : public Item {
public:
	RefrigeratedItem(int id, double weight, int count, int containerId) : Item(id, weight, count, containerId) {}
	double getTotalWeight() const override { return weight * count; }

	string getType() const override { 
		return "Refrigerated"; 
	}
};
class LiquidItem : public Item {
public:
	LiquidItem(int id, double weight, int count, int containerId) : Item(id, weight, count, containerId) {}
	double getTotalWeight() const override { return weight * count; }

	string getType() const override { 
		return "Liquid"; 
	}
};


class FactoryItem {
public: 
	static unique_ptr<Item> createItem(const string& type, int id, double weight, int count, int containerId) {
		if (type == "Small") return make_unique<SmallItem>(id, weight, count, containerId);
		else if (type == "Heavy") return make_unique<HeavyItem>(id, weight, count, containerId);
		else if (type == "Refrigerated") return make_unique<RefrigeratedItem>(id, weight, count, containerId);
		else if (type == "<Liquid") return make_unique<LiquidItem>(id, weight, count, containerId);
	
		throw invalid_argument("Invalid item type");
	}


};

int main() {

	LightWeightShipFactory lightFactory;

	Port port1(1, 34.55, -120.32);
	Port port2(2, 34.60, -120.35);

	CapacityLimits ship1(10000, 10, 3, 3, 3);
	CapacityLimits ship2(10000, 8, 2, 2, 2);

	Ship myship(1, 50000, &port1, ship1, 0.6);
	Ship friendShip(2, 30000, &port1, ship2, 1.3);

	auto container1 = make_unique<BasicContainer>(101, 2500);
	auto container2 = make_unique<BasicContainer>(102, 2500);
	auto container3 = make_unique<HeavyContainer>(111, 3500);
	auto container4 = make_unique<HeavyContainer>(112, 4000);


	auto item = FactoryItem::createItem("Small", 5, 15.4, 4, 101);
	cout << "Item created: " << item->getType() << ", Weight: " << item->getTotalWeight() << endl;


	myship.load(move(container1));
	myship.load(move(container3));
	myship.load(move(container4));
	friendShip.load(move(container2));

	Main::sailToPort(myship, port2);
	Main::sailToPort(friendShip, port2);

	Main::printCurrentContainers(myship);

	Main::printCurrentContainers(friendShip);

	myship.unload(port2, make_unique<BasicContainer>(101, 2500));

	myship.reFuel(5000);

	Main::displayContainersAtCurrentPort(port2);

	Main::printCurrentContainers(myship);


	cout << endl << endl;

	
	auto lightShip = lightFactory.createShip(1, &port1, 10000);
	port1.incomingShip(lightShip.get());


	MediumWeightShipBuilder mediumBuilder(2, 20000, &port1);
	mediumBuilder.setCapacityLimits(CapacityLimits(15000, 10, 5, 2, 1));
	auto mediumShip = mediumBuilder.getResult();
	port1.incomingShip(mediumShip.get());

	Main::printCurrentContainers(*lightShip);
	Main::printCurrentContainers(*mediumShip);

	auto container10 = FactoryItem::createItem("Small", 101, 1000, 10, 1);
	auto container20 = FactoryItem::createItem("Heavy", 102, 5000, 1, 2);
	auto container30 = FactoryItem::createItem("Refrigerated", 103, 7000, 1, 3);

	if (lightShip->load(make_unique<BasicContainer>(1, 3000))) {
		cout << "Loaded BasicContainer onto LightWeightShip.\n";
	}
	if (mediumShip->load(make_unique<HeavyContainer>(2, 4000))) {
		cout << "Loaded HeavyContainer onto MediumWeightShip.\n";
	}

	Main::sailToPort(*lightShip, port2);
	Main::sailToPort(*mediumShip, port2);

	lightShip->unload(port2, make_unique<BasicContainer>(1, 3000));
	mediumShip->unload(port2, make_unique<HeavyContainer>(2, 4000));

	Main::displayContainersAtCurrentPort(port2);


	return 0;


}


