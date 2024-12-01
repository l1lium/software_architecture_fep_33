#include <iostream>
#include <string>
#include <unordered_map>

using namespace std;


// Singleton Template Base Class
template <typename T>
class Singleton {
public:
    static T& getInstance() {
        static T instance;
        return instance;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

protected:
    Singleton() {}
};



// SettingsManager Singleton Class
class SettingsManager : public Singleton<SettingsManager> {
   
    friend class Singleton<SettingsManager>;
    int preferredTemperature = 22; 
private:
    unordered_map<string, string> settings;
public:

    void setSetting(const string& key, const string& value) {
        settings[key] = value;
        cout << "Setting updated: " << key << " = " << value << endl;
    }
    void displaySettings() {
        cout << "Current settings:" << endl;
        for (const auto& pair : settings) {
            cout << pair.first << " = " << pair.second << endl;
        }
    }
    void setPreferredTemperature(int temp) { 
        preferredTemperature = temp;
    }
    int getPreferredTemperature() const { 
        return preferredTemperature; 
    }
};

// EnergyManager Singleton Class
class EnergyManager : public Singleton<EnergyManager> {
    friend class Singleton<EnergyManager>;

public:
    void monitorUsage() { std::cout << "Monitoring energy usage...\n"; }
    void optimizeEnergy() { std::cout << "Optimizing energy usage...\n"; }
};

// LightingSystem Class
class LightingSystem {
public:
    void turnOnLights() { std::cout << "Lights are turned on.\n"; }
    void turnOffLights() { std::cout << "Lights are turned off.\n"; }
    void setBrightness(int level) { std::cout << "Setting brightness to " << level << "%.\n"; }
};

// SecuritySystem Class
class SecuritySystem {
public:
    void armSystem() { std::cout << "Security system armed.\n"; }
    void disarmSystem() { std::cout << "Security system disarmed.\n"; }
    void triggerAlarm() { std::cout << "Alarm triggered!\n"; }
};

// ClimateControlSystem Class
class ClimateControlSystem {
public:
    void setTemperature(int temp) { std::cout << "Setting temperature to " << temp << "°C.\n"; }
    void turnOnHeater() { std::cout << "Heater turned on.\n"; }
    void turnOnAC() { std::cout << "AC turned on.\n"; }
};

// EntertainmentSystem Class
class EntertainmentSystem {
public:
    void playMusic() { std::cout << "Playing music...\n"; }
    void stopMusic() { std::cout << "Music stopped.\n"; }
    void setVolume(int level) { std::cout << "Setting volume to " << level << ".\n"; }
};

// Appliance Interface - for Bridge Pattern
class Appliance {
public:
    virtual void start() = 0;
    virtual void stop() = 0;
    virtual ~Appliance() {}
};

// Concrete Appliance Implementations
class AC : public Appliance {
public:
    void start() override { 
        cout << "AC is now ON.\n";
    }
    void stop() override { 
        cout << "AC is now OFF.\n"; 
    }
};

class Refrigerator : public Appliance {
public:
    void start() override { 
        cout << "Refrigerator is now ON.\n"; 
    }
    void stop() override { 
        cout << "Refrigerator is now OFF.\n"; 
    }
};

// Controller Abstraction - Bridge Pattern
class Controller {
protected:
    Appliance* appliance;

public:
    Controller(Appliance* appliance) : appliance(appliance) {}
    virtual void turn_on() = 0;
    virtual void turn_off() = 0;
    virtual ~Controller() {}
};

// Concrete Controllers
class AutomaticRemoteController : public Controller {
public:
    AutomaticRemoteController(Appliance* appliance) : Controller(appliance) {}
    void turn_on() override { appliance->start(); }
    void turn_off() override { appliance->stop(); }
};

class ManualRemoteController : public Controller {
public:
    ManualRemoteController(Appliance* appliance) : Controller(appliance) {}
    void turn_on() override { appliance->start(); }
    void turn_off() override { appliance->stop(); }
};

// SmartHomeFacade Class - Facade Pattern
class SmartHomeFacade {
    LightingSystem lighting;
    SecuritySystem security;
    ClimateControlSystem climate;
    EntertainmentSystem entertainment;
    SettingsManager& settings = SettingsManager::getInstance();

public:
    void activateSecuritySystem() {
        security.armSystem();
    }

    void setClimateControl(int targetTemp) {
        climate.setTemperature(targetTemp);
        if (targetTemp > settings.getPreferredTemperature()) {
            climate.turnOnAC();
        }
        else {
            climate.turnOnHeater();
        }
    }

    void controlLighting(bool on, int brightness) {
        if (on) {
            lighting.turnOnLights();
            lighting.setBrightness(brightness);
        }
        else {
            lighting.turnOffLights();
        }
    }

    void playMusic(int volume) {
        entertainment.playMusic();
        entertainment.setVolume(volume);
    }

    void stopMusic() {
        entertainment.stopMusic();
    }
};

// VoiceControl Class
class VoiceControl {
    SmartHomeFacade& facade;

public:
    VoiceControl(SmartHomeFacade& facadeRef) : facade(facadeRef) {}

    void processCommand(const std::string& command) {
        if (command == "Turn on the lights") {
            facade.controlLighting(true, 75);
        }
        else if (command == "Turn off the lights") {
            facade.controlLighting(false, 0);
        }
        else if (command == "Set temperature to 22") {
            facade.setClimateControl(22);
        }
        else if (command == "Play music") {
            facade.playMusic(50);
        }
        else if (command == "Stop music") {
            facade.stopMusic();
        }
        else {
            std::cout << "Unknown command.\n";
        }
    }
};

// Main function to demonstrate the system
int main() {
    // Instantiate the facade
    SmartHomeFacade smartHome;
    VoiceControl voiceControl(smartHome);

    // Simulating commands
    voiceControl.processCommand("Turn on the lights");
    voiceControl.processCommand("Set temperature to 22");
    voiceControl.processCommand("Play music");
    voiceControl.processCommand("Stop music");

    // Using EnergyManager directly (Singleton)
    EnergyManager::getInstance().monitorUsage();
    EnergyManager::getInstance().optimizeEnergy();

    // Bridge Pattern: Controlling appliances with different controllers
    AC ac;
    Refrigerator refrigerator;

    AutomaticRemoteController autoController(&ac);
    ManualRemoteController manualController(&refrigerator);

    autoController.turn_on(); // AC is now ON
    autoController.turn_off(); // AC is now OFF

    manualController.turn_on(); // Refrigerator is now ON
    manualController.turn_off(); // Refrigerator is now OFF

    return 0;
}

