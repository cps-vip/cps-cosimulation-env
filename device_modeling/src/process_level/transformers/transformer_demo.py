
from transformer_device import Transformer  

# Instantiate a Transformer
transformer = Transformer(name="Transformer1", communication_protocol="IEC61850", transformer_type="Distribution Transformer")

# Set transformer parameters
transformer.set_primary_voltage(10000.0)  # Set primary voltage to 10 kV
transformer.set_taps([0, 1, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50])  # Set secondary voltage to 400 V
transformer.set_tap(5)  # Assuming 11 taps available
transformer.set_secondary_voltage()

# Display transformer details
print(f"Transformer Name: {transformer.name}")
print(f"Primary Voltage: {transformer.get_primary_voltage()} V")
print(f"Secondary Voltage: {transformer.get_secondary_voltage()} V")
print(f"Tap Position: {transformer.tap_position}")
print(f"Available Taps: {transformer.get_taps()}")

# Demonstrate adjusting voltage
adjustment = 2  # Increase tap position by 2
transformer.adjust_voltage(adjustment)

# Display updated details after voltage adjustment
print("\nAfter Voltage Adjustment:")
print(f"Tap Position: {transformer.get_tap()}")
print(f"Adjusted Secondary Voltage: {transformer.get_secondary_voltage()} V")
print(f"Output Voltage: {transformer.get_output_voltage()} V")
print(f"Available Taps: {transformer.get_taps()}")