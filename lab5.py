from abc import ABC, abstractmethod

# Singleton MetaClass
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# SettingsManager (Singleton)
class SettingsManager(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {
            "preferred_temperature": 22,
            "lighting_preset": 50,
        }

    def set_setting(self, key, value):
        self.settings[key] = value

    def get_setting(self, key):
        return self.settings.get(key)

# EnergyManager (Singleton)
class EnergyManager(metaclass=SingletonMeta):
    def monitor_usage(self):
        print("Monitoring energy usage...")

    def optimize_energy(self):
        print("Optimizing energy usage...")

# Subsystems
class LightingSystem:
    def turn_on_lights(self):
        print("Lights are ON")

    def turn_off_lights(self):
        print("Lights are OFF")

    def set_brightness(self, level):
        print(f"Lights brightness set to {level}%")

class SecuritySystem:
    def arm_system(self):
        print("Security system is ARMED")

    def disarm_system(self):
        print("Security system is DISARMED")

    def trigger_alarm(self):
        print("ALARM triggered!")

class ClimateControlSystem:
    def set_temperature(self, target_temp):
        print(f"Temperature set to {target_temp}°C")

    def turn_on_heater(self):
        print("Heater is ON")

    def turn_on_ac(self):
        print("Air conditioning is ON")

class EntertainmentSystem:
    def play_music(self):
        print("Playing music...")

    def stop_music(self):
        print("Music stopped.")

    def set_volume(self, level):
        print(f"Volume set to {level}")

# Facade
class SmartHomeFacade:
    def __init__(self):
        self.lighting = LightingSystem()
        self.security = SecuritySystem()
        self.climate = ClimateControlSystem()
        self.entertainment = EntertainmentSystem()
        self.settings = SettingsManager()

    def activate_security_system(self):
        self.security.arm_system()

    def set_climate_control(self, target_temp):
        self.climate.set_temperature(target_temp)

    def control_lighting(self, brightness_level):
        self.lighting.set_brightness(brightness_level)

    def play_music(self):
        self.entertainment.play_music()

# Bridge Pattern
class Appliance(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class LightAppliance(Appliance):
    def start(self):
        print("Light is ON")

    def stop(self):
        print("Light is OFF")

class ACAppliance(Appliance):
    def start(self):
        print("AC is ON")

    def stop(self):
        print("AC is OFF")

class Switch:
    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def turn_on(self):
        self.appliance.start()

    def turn_off(self):
        self.appliance.stop()

# Example Usage
def main():
    # Using the facade
    smart_home = SmartHomeFacade()
    smart_home.activate_security_system()
    smart_home.set_climate_control(24)
    smart_home.control_lighting(75)
    smart_home.play_music()

    # Using the bridge
    light = LightAppliance()
    light_switch = Switch(light)
    light_switch.turn_on()
    light_switch.turn_off()

    ac = ACAppliance()
    ac_switch = Switch(ac)
    ac_switch.turn_on()
    ac_switch.turn_off()

if __name__ == "__main__":
    main()
