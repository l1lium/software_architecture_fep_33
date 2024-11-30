# Singleton Pattern Implementation
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Settings Manager (Singleton)
class SettingsManager(metaclass=SingletonMeta):
    def __init__(self):
        self.temperature = 72
        self.lighting_mode = "default"

    def set_temperature(self, temp):
        self.temperature = temp
        print(f"Temperature set to {temp}°F")

    def get_temperature(self):
        return self.temperature


# Energy Manager (Singleton)
class EnergyManager(metaclass=SingletonMeta):
    def monitor_usage(self):
        print("Monitoring energy usage...")

    def optimize_energy(self):
        print("Optimizing energy usage...")


# Facade Pattern Implementation
class SmartHomeFacade:
    def __init__(self):
        self.lighting = LightingSystem()
        self.security = SecuritySystem()
        self.climate = ClimateControlSystem()
        self.entertainment = EntertainmentSystem()
        self.energy_manager = EnergyManager()
        self.settings = SettingsManager()

    def activate_security_system(self):
        self.security.arm_system()

    def set_climate_control(self, temp):
        self.settings.set_temperature(temp)
        self.climate.set_temperature(temp)

    def control_lighting(self, mode):
        self.lighting.set_brightness(mode)


# Lighting System
class LightingSystem:
    def turn_on_lights(self):
        print("Lights are turned on.")

    def turn_off_lights(self):
        print("Lights are turned off.")

    def set_brightness(self, level):
        print(f"Setting brightness to {level}.")


# Security System
class SecuritySystem:
    def arm_system(self):
        print("Security system armed.")

    def disarm_system(self):
        print("Security system disarmed.")

    def trigger_alarm(self):
        print("Alarm triggered!")


# Climate Control System
class ClimateControlSystem:
    def set_temperature(self, target_temp):
        print(f"Setting temperature to {target_temp}°F.")

    def turn_on_heater(self):
        print("Heater turned on.")

    def turn_on_ac(self):
        print("AC turned on.")


# Entertainment System
class EntertainmentSystem:
    def play_music(self):
        print("Playing music.")

    def stop_music(self):
        print("Music stopped.")

    def set_volume(self, level):
        print(f"Volume set to {level}.")


# Voice Control
class VoiceControl:
    def __init__(self, facade: SmartHomeFacade):
        self.facade = facade

    def execute_command(self, command: str):
        if "lights on" in command.lower():
            self.facade.control_lighting("on")
        elif "lights off" in command.lower():
            self.facade.control_lighting("off")
        elif "set temperature" in command.lower():
            temp = int(command.split()[-1])
            self.facade.set_climate_control(temp)
        elif "arm security" in command.lower():
            self.facade.activate_security_system()
        else:
            print("Unknown command.")


# Bridge Pattern Implementation
class Appliance:
    def start(self):
        print("Appliance started.")

    def stop(self):
        print("Appliance stopped.")


class AC(Appliance):
    def start(self):
        print("AC is cooling the room.")

    def stop(self):
        print("AC stopped.")


class Refrigerator(Appliance):
    def start(self):
        print("Refrigerator is running.")

    def stop(self):
        print("Refrigerator is off.")


class Fan(Appliance):
    def start(self):
        print("Fan is circulating air.")

    def stop(self):
        print("Fan stopped.")


class TV(Appliance):
    def start(self):
        print("TV is now on.")

    def stop(self):
        print("TV is off.")


class GateOpener(Appliance):
    def start(self):
        print("Gate is opening.")

    def stop(self):
        print("Gate stopped.")


# Remote Controllers
class RemoteController:
    def __init__(self, appliance):
        self.appliance = appliance

    def turn_on(self):
        self.appliance.start()

    def turn_off(self):
        self.appliance.stop()


# Switch to control appliances
class Switch:
    def __init__(self):
        self.appliances = []

    def add_appliance(self, appliance):
        self.appliances.append(appliance)

    def control_appliances(self):
        for appliance in self.appliances:
            appliance.start()


# Example Testing
if __name__ == "__main__":
    # Testing Facade pattern
    home_facade = SmartHomeFacade()
    home_facade.control_lighting("dim")
    home_facade.set_climate_control(68)
    home_facade.activate_security_system()

    # Testing Bridge pattern with appliances and remote controllers
    ac = AC()
    fridge = Refrigerator()
    fan = Fan()

    ac_remote = RemoteController(ac)
    fridge_remote = RemoteController(fridge)

    ac_remote.turn_on()
    fridge_remote.turn_off()

    switch = Switch()
    switch.add_appliance(ac)
    switch.add_appliance(fridge)
    switch.control_appliances()

    # Testing Voice Control
    voice_control = VoiceControl(home_facade)
    voice_control.execute_command("Turn lights on")
    voice_control.execute_command("Set temperature to 72")
    voice_control.execute_command("Arm security system")
