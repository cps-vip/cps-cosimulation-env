# Run under "device_modeling" folder: python3 src/bay_controller_demo.py

from bay_level.bay_device import BayDevice
from bay_level.bay_controllers import BayController
import time

# Create a BayController
bay_controller = BayController("Demo Bay")

# Create some BayDevices and add them to the BayController
device1 = BayDevice("Load1", "IEC61850", "Power Bay")
device2 = BayDevice("Generator1", "Modbus", "Power Bay")

bay_controller.add_device(device1)
bay_controller.add_device(device2)

# Set the target voltage for the bay
bay_controller.set_target_voltage(600.0)

# Specify the time range for data collection
start_time = 0
end_time   = 30

# Simulate the bay's operation and voltage regulation
print(f"Bay Status: {bay_controller.get_bay_status()}")
time.sleep(1)  # Simulating a delay

# Activate Device1
device1.activate()
print(f"Activated {device1.get_device_name()}")
time.sleep(1)

for t in range(start_time, end_time + 1):
    bay_controller.regulate_voltage()
    time.sleep(1)

# Deactivate Device1
device1.deactivate()
print(f"Deactivated {device1.get_device_name()}")
time.sleep(1)

# Visualize voltage history as a continuous line during the specified time period
bay_controller.visualize_voltage_history(start_time, end_time)