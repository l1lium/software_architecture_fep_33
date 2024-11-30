# Singleton Pattern Implementation
class SingletonMeta(type):
    """A metaclass for Singleton implementation."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SettingsManager(metaclass=SingletonMeta):
    """Singleton for managing global settings."""
    def __init__(self):
        self.settings = {
            "preferred_temperature": 22,
            "lighting_mode": "default",
            "volume_level": 50,
        }

    def update_setting(self, key, value):
        self.settings[key] = value

    def get_setting(self, key):
        return self.settings.get(key, None)


class EnergyManager(metaclass=SingletonMeta):
    """Singleton for managing energy usage."""
    def monitor_usage(self):
        print("Monitoring energy usage...")

    def optimize_energy(self):
        print("Optimizing energy consumption...")

# Subsystems for Facade
class LightingSystem:
    def turn_on_lights(self):
        print("Lights turned on.")

    def turn_off_lights(self):
        print("Lights turned off.")

    def set_brightness(self, level):
        print(f"Brightness set to {level}.")


class SecuritySystem:
    def arm_system(self):
        print("Security system armed.")

    def disarm_system(self):
        print("Security system disarmed.")

    def trigger_alarm(self):
        print("Alarm triggered!")


class ClimateControlSystem:
    def set_temperature(self, target_temp):
        print(f"Temperature set to {target_temp}°C.")

    def turn_on_ac(self):
        print("AC turned on.")

    def turn_on_heater(self):
        print("Heater turned on.")


class EntertainmentSystem:
    def play_music(self):
        print("Playing music.")

    def stop_music(self):
        print("Music stopped.")

    def set_volume(self, level):
        print(f"Volume set to {level}.")


# Facade Pattern Implementation
class SmartHomeFacade:
    """Central interface for controlling all subsystems."""
    def __init__(self):
        self.lighting = LightingSystem()
        self.security = SecuritySystem()
        self.climate = ClimateControlSystem()
        self.entertainment = EntertainmentSystem()
        self.settings = SettingsManager()
        self.energy = EnergyManager()

    def activate_security_system(self):
        self.security.arm_system()

    def control_lighting(self, action, brightness=None):
        if action == "on":
            self.lighting.turn_on_lights()
        elif action == "off":
            self.lighting.turn_off_lights()
        if brightness is not None:
            self.lighting.set_brightness(brightness)

    def set_climate_control(self, target_temp):
        self.climate.set_temperature(target_temp)

    def optimize_energy(self):
        self.energy.optimize_energy()

    def play_music(self):
        self.entertainment.play_music()

    def stop_music(self):
        self.entertainment.stop_music()


# Bridge Pattern Implementation
class Switch:
    """Abstract switch for controlling appliances."""
    def __init__(self, appliance):
        self.appliance = appliance

    def turn_on(self):
        self.appliance.start()

    def turn_off(self):
        self.appliance.stop()


class RemoteController(Switch):
    """Remote Controller, extension of Switch."""
    def increase_setting(self, setting, amount):
        print(f"Increasing {setting} by {amount}.")

    def decrease_setting(self, setting, amount):
        print(f"Decreasing {setting} by {amount}.")


class Appliance:
    """Abstract Appliance."""
    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class Light(Appliance):
    def start(self):
        print("Light is on.")

    def stop(self):
        print("Light is off.")


class Heater(Appliance):
    def start(self):
        print("Heater is warming.")

    def stop(self):
        print("Heater is off.")


# Testing all patterns
if __name__ == "__main__":
    # Testing Facade and Singleton
    smart_home = SmartHomeFacade()
    smart_home.control_lighting(action="on", brightness=70)
    smart_home.set_climate_control(target_temp=24)
    smart_home.activate_security_system()
    smart_home.play_music()
    smart_home.optimize_energy()

    # Testing Bridge
    light = Light()
    heater = Heater()

    light_switch = Switch(light)
    heater_remote = RemoteController(heater)

    light_switch.turn_on()
    heater_remote.turn_on()
    heater_remote.turn_off()