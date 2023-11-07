from typing import List

class Transformer:
    def __init__(self, name: str, communication_protocol: str, transformer_type: str):
        self.name = name
        self.communication_protocol = communication_protocol
        self.transformer_type = transformer_type
        self.primary_voltage: float = 0.0
        self.secondary_voltage: float = 0.0
        self.tap_position: int = 0
        self.taps: List[int] = []


    def set_primary_voltage(self, voltage: float) -> None:
        self.primary_voltage = voltage


    def get_primary_voltage(self) -> float:
        return self.primary_voltage


    def set_secondary_voltage(self, voltage: float) -> None:
        self.secondary_voltage = voltage


    def get_secondary_voltage(self) -> float:
        return self.secondary_voltage


    def set_tap(self, position: int) -> None:
        if 0 <= position < len(self.taps):
            self.tap_position = position
        else:
            print("Invalid tap position. Tap position remains unchanged.")


    def get_tap(self) -> int:
        return self.tap_position


    def set_taps(self, num_taps: int) -> None:
        self.taps = list(range(num_taps))


    def get_taps(self) -> List[int]:
        return self.taps

    def set_state(self, primary_voltage: float, secondary_voltage: float, tap: int, num_taps: int) -> None:
        self.set_primary_voltage(primary_voltage)
        self.set_secondary_voltage(secondary_voltage)
        self.set_tap(tap)
        self.set_taps(num_taps)


    def get_transformer_type(self) -> str:
        return self.transformer_type


    def get_turns_ratio(self) -> int:
        return self.taps[self.tap_position]


    def get_output_voltage(self) -> float:
        return self.primary_voltage * self.get_turns_ratio()


    def adjust_voltage(self, adjustment: int) -> None:
        new_tap_position = self.tap_position + adjustment
        if 0 <= new_tap_position < len(self.taps):
            self.tap_position = new_tap_position
            self.secondary_voltage = self.primary_voltage * self.get_turns_ratio()
        else:
            print("Voltage adjustment not possible. Tap position remains unchanged.")