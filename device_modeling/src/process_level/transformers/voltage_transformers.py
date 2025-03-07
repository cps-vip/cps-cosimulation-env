from .transformer_device import Transformer

class PowerTransformer(Transformer):
    def __init__(self, name: str):
        self.name = name
        self.transformer_type = "Current Transformer"

        self.primary_voltage: float = 0.0 #input voltage
        self.secondary_voltage: float = 0.0 #output voltage
        self.tap_position: float = 1.0

    def set_primary_voltage(self, voltage: float) -> None:
        if voltage <= 0:
            raise ValueError("Voltage need to set other than zero")
        self.primary_voltage = voltage

    def get_primary_voltage(self) -> float:
        return self.primary_voltage

    def set_secondary_voltage(self) -> None:
        if self.primary_voltage == 0.0:
            raise ValueError("Primary voltage is not set.")

        if not self.taps:
            raise ValueError("Turn ratio is not set.")

        # Calculate the secondary voltage using primary voltage and current turn ratio
        secondary_voltage = self.primary_voltage * self.get_turns_ratio()

        # Set the calculated secondary voltage
        self.secondary_voltage = secondary_voltage


    def get_secondary_voltage(self) -> float:
        return self.secondary_voltage


    def set_state(self, primary_voltage: float, secondary_voltage: float, tap: int, num_taps: int) -> None:
        self.set_primary_voltage(primary_voltage)
        self.set_secondary_voltage(secondary_voltage)
        self.set_tap(tap)
        self.set_taps(num_taps)
        
    def get_output_voltage(self) -> float:
        return self.get_primary_voltage()

    def adjust_voltage(self, desired_voltage: float) -> None:
        ratio = desired_voltage/self.get_primary_voltage
        self.set_tap(ratio)
        self.set_secondary_voltage()