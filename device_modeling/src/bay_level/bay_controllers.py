from src.bay_level.bay_device import BayDevice
import random
import matplotlib.pyplot as plt

class BayController:
    def __init__(self, name: str):
        self.name = name
        self.devices = []  # List to store BayDevice objects
        self.target_voltage = 0.0  # The desired target voltage for the bay
        self.voltage_margin = 0.1  # A margin for acceptable voltage variation
        self.voltage_history = []  # Store voltage history for visualization


    def add_device(self, device: BayDevice):
        self.devices.append(device)

    def remove_device(self, device: BayDevice):
        if device in self.devices:
            self.devices.remove(device)


    def get_device_names(self) -> list:
        return [device.get_device_name() for device in self.devices]


    def get_bay_status(self) -> str:
        # A bay's status could be determined by the status of its devices.
        # For simplicity, we assume the bay is active if at least one device is active.
        for device in self.devices:
            if device.get_status() == "Active":
                return "Active"
        return "Inactive"


    def set_target_voltage(self, voltage: float):
        self.target_voltage = voltage


    def regulate_voltage(self):
        for device in self.devices:
            if device.get_status() == "Active":
                # Check the voltage of each active device
                if device.get_communication_protocol() == "IEC61850":
                    # Assuming IEC61850 protocol for voltage regulation
                    current_voltage = self.measure_voltage(device)
                    self.voltage_history.append(current_voltage)  # Log voltage
                    if abs(current_voltage - self.target_voltage) > self.voltage_margin:
                        # Implement voltage regulation control logic
                        print(f"Voltage regulation for {device.get_device_name()} required.")
                        self.send_voltage_regulation_command(device, self.target_voltage)
                    else:
                        print(f"{device.get_device_name()} voltage within acceptable range.")
                else:
                    print(f"{device.get_device_name()} does not use IEC61850 protocol.")


    def measure_voltage(self, device: BayDevice) -> float:
        # Simulate measuring the voltage of a device
        voltage_min = self.target_voltage - self.voltage_margin
        voltage_max = self.target_voltage + self.voltage_margin
        voltage = random.uniform(voltage_min, voltage_max)
        return voltage


    def send_voltage_regulation_command(self, device: BayDevice, target_voltage: float):
        # Simulate sending a voltage regulation command to the IEC61850 device
        print(f"Sent voltage regulation command to {device.get_device_name()}")


    def visualize_voltage_history(self):
        if self.voltage_history:
            plt.figure()
            plt.plot(range(len(self.voltage_history)), self.voltage_history)
            plt.xlabel("Time")
            plt.ylabel("Voltage Level")
            plt.title(f"{self.name} Voltage History")
            plt.show()