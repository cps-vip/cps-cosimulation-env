from bay_level.bay_device import BayDevice
import random
import matplotlib.pyplot as plt

class BayController:
    def __init__(self, name: str):
        """
        Constructor for the BayController class.
        
        Initializes the BayController object with a name, an empty list to store BayDevice objects,
        a target voltage, a voltage margin for acceptable voltage variation, and an empty voltage history.

        Args:
            name (str): The name of the bay controller.
        """
        self.name = name
        self.devices = []          # List to store BayDevice objects
        self.target_voltage = 0.0  # The desired target voltage for the bay
        self.voltage_margin = 5.0  # A margin for acceptable voltage variation
        self.voltage_history = []  # Store voltage history for visualization


    def add_device(self, device: BayDevice):
        """
        Method to add a BayDevice object to the list of devices.

        Args:
            device (BayDevice): The BayDevice object to add.
        """
        self.devices.append(device)


    def remove_device(self, device: BayDevice):
        """
        Method to remove a BayDevice object from the list of devices.

        Args:
            device (BayDevice): The BayDevice object to remove.
        """
        if device in self.devices:
            self.devices.remove(device)


    def get_device_names(self) -> list:
        """
        Method to get the names of all devices in the bay.

        Returns:
            list: A list of device names.
        """
        return [device.get_device_name() for device in self.devices]


    def get_bay_status(self) -> str:
        """
        Method to determine the bay's status based on the status of its devices.

        Returns:
            str: "Active" if at least one device is active, otherwise "Inactive."
        """
        for device in self.devices:
            if device.get_status() == "Active":
                return "Active"
        return "Inactive"


    def set_target_voltage(self, voltage: float):
        """
        Method to set the desired target voltage for the bay.

        Args:
            voltage (float): The target voltage.
        """
        self.target_voltage = voltage


    def regulate_voltage(self):
        """
        Method to regulate the voltage in the bay by checking and adjusting the voltage of active devices
        only when it goes out of the target voltage range plus the margin.
        """
        for device in self.devices:
            if device.get_status() == "Active":
                # Check the voltage of each active device
                if device.get_communication_protocol() == "IEC61850":
                    # Assuming IEC61850 protocol for voltage regulation
                    current_voltage = self.simulate_voltage(device)
                    self.voltage_history.append(current_voltage)  # Log voltage
                    voltage_difference = current_voltage - self.target_voltage

                    if abs(voltage_difference) > self.voltage_margin:
                        # Implement voltage regulation control logic only when out of acceptable range
                        if voltage_difference > 0:
                            # Voltage is too high, reduce it
                            reduction_amount = min(voltage_difference, self.voltage_margin)
                            new_voltage = current_voltage - reduction_amount
                            print(f"Reducing voltage for {device.get_device_name()} by {reduction_amount} V.")
                        else:
                            # Voltage is too low, increase it
                            increase_amount = min(-voltage_difference, self.voltage_margin)
                            new_voltage = current_voltage + increase_amount
                            print(f"Increasing voltage for {device.get_device_name()} by {increase_amount} V.")

                        # Set the target voltage of the device to maintain it
                        #device.target_voltage = new_voltage
                        #self.voltage_history[-1] = new_voltage  # Update the last recorded voltage with the adjusted voltage
                        self.voltage_history.append(new_voltage)

                    else:
                        print(f"{device.get_device_name()} voltage within acceptable range.")
                else:
                    print(f"{device.get_device_name()} does not use IEC61850 protocol.")


    def simulate_voltage(self, device: BayDevice) -> float:
        """
        Method to simulate measuring the voltage of a device.

        Args:
            device (BayDevice): The device for which voltage is measured.

        Returns:
            float: The simulated voltage reading.
        """
        # Simulate measuring the voltage of a device
        voltage_min = self.target_voltage - self.voltage_margin * 2
        voltage_max = self.target_voltage + self.voltage_margin * 2
        voltage = random.uniform(voltage_min, voltage_max)
        return voltage


    def send_voltage_regulation_command(self, device: BayDevice, target_voltage: float, current_voltage: float):
        """
        Method to send a voltage regulation command to an IEC61850 device and adjust the voltage to keep it within an acceptable range.

        Args:
            device (BayDevice): The device to which the command is sent.
            target_voltage (float): The target voltage to maintain.
            current_voltage (float): The current voltage of the device.
        """
        voltage_difference = current_voltage - target_voltage

        if abs(voltage_difference) > self.voltage_margin:
            if voltage_difference > 0:
                # Voltage is too high, reduce it
                reduction_amount = min(voltage_difference, self.voltage_margin)
                new_voltage = current_voltage - reduction_amount
                print(f"Reducing voltage for {device.get_device_name()} by {reduction_amount} V.")
            else:
                # Voltage is too low, increase it
                increase_amount = min(-voltage_difference, self.voltage_margin)
                new_voltage = current_voltage + increase_amount
                print(f"Increasing voltage for {device.get_device_name()} by {increase_amount} V.")
        
            # Set the target voltage of the device to maintain it
            device.target_voltage = new_voltage
            self.voltage_history[-1] = new_voltage  # Update the last recorded voltage with the adjusted voltage

        else:
            print(f"{device.get_device_name()} voltage within acceptable range.")


    def visualize_voltage_history(self, start_time, end_time):
        """
        Method to visualize the voltage history of the bay with voltage values displayed as a continuous line during a time period,
        along with regulated upper and lower ranges.

        Args:
            start_time (int): The starting time (in seconds) for the visualization.
            end_time (int): The ending time (in seconds) for the visualization.
        """
        if self.voltage_history:
            plt.figure()
            plt.xlabel("Time (s)")
            plt.ylabel("Voltage Level (V)")
            plt.title(f"{self.name} Voltage History")

            # Find the indices corresponding to the specified time period
            start_index = int(start_time)
            end_index = int(end_time)

            # Display voltage values as a continuous line during the specified time period
            if start_index < len(self.voltage_history) and end_index < len(self.voltage_history):
                time_range = range(start_index, end_index)
                voltage_range = self.voltage_history[start_index:end_index]

                plt.plot(time_range, voltage_range, label="Voltage Level (V)")

                # Calculate regulated upper and lower ranges
                upper_range = [self.target_voltage + self.voltage_margin] * len(time_range)
                lower_range = [self.target_voltage - self.voltage_margin] * len(time_range)

                plt.plot(time_range, upper_range, '--', label="Upper Range (V)", color='red')
                plt.plot(time_range, lower_range, '--', label="Lower Range (V)", color='green')

            plt.legend()
            plt.show()