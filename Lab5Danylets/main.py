class SettingsManager:
    """Singleton for managing global settings."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance.settings = {
                "preferred_temperature": 22,
                "lighting_preset": "Warm",
            }
        return cls._instance

class EnergyManager:
    """Singleton for managing energy usage."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnergyManager, cls).__new__(cls)
        return cls._instance

    def monitor_usage(self):
        return "Monitoring energy usage across devices."

    def optimize_energy(self):
        return "Optimizing energy consumption."

class LightingSystem:
    def turn_on_lights(self):
        return "Lights turned on."

    def turn_off_lights(self):
        return "Lights turned off."

    def set_brightness(self, level):
        return f"Brightness set to {level}."

class SecuritySystem:
    def arm_system(self):
        return "Security system armed."

    def disarm_system(self):
        return "Security system disarmed."

    def trigger_alarm(self):
        return "Alarm triggered!"

class ClimateControlSystem:
    def set_temperature(self, target_temp):
        return f"Temperature set to {target_temp}°C."

    def turn_on_heater(self):
        return "Heater turned on."

    def turn_on_ac(self):
        return "Air conditioning turned on."

class EntertainmentSystem:
    def play_music(self):
        return "Playing music."

    def stop_music(self):
        return "Music stopped."

    def set_volume(self, level):
        return f"Volume set to {level}."

class SmartHomeFacade:
    def __init__(self):
        self.lighting = LightingSystem()
        self.security = SecuritySystem()
        self.climate = ClimateControlSystem()
        self.entertainment = EntertainmentSystem()

    def activate_security_system(self):
        return self.security.arm_system()

    def set_climate_control(self, temperature):
        return self.climate.set_temperature(temperature)

    def control_lighting(self, action):
        if action == "on":
            return self.lighting.turn_on_lights()
        elif action == "off":
            return self.lighting.turn_off_lights()
        return "Invalid action for lighting."

class Appliance:
    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

class Fan(Appliance):
    def start(self):
        return "Fan started."

    def stop(self):
        return "Fan stopped."

class Light(Appliance):
    def start(self):
        return "Light switched on."

    def stop(self):
        return "Light switched off."

class Switch:
    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def turn_on(self):
        return self.appliance.start()

    def turn_off(self):
        return self.appliance.stop()

if __name__ == "__main__":
    smart_home = SmartHomeFacade()
    print("\nFacade Pattern Testing:")
    print(smart_home.activate_security_system())
    print(smart_home.set_climate_control(24))
    print(smart_home.control_lighting("on"))

    fan = Fan()
    fan_switch = Switch(fan)
    print("\nBridge Pattern Testing:")
    print(fan_switch.turn_on())
    print(fan_switch.turn_off())

    light = Light()
    light_switch = Switch(light)
    print(light_switch.turn_on())
    print(light_switch.turn_off())
