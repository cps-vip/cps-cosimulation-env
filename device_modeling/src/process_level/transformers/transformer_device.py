from typing import List

class Transformer:
    def __init__(self, name: str, communication_protocol: str, transformer_type: str):
        """
        Initializes a Transformer object with the specified name, communication protocol, and transformer type.
        
        Args:
            name (str): The name of the transformer.
            communication_protocol (str): The communication protocol used by the transformer.
            transformer_type (str): The type or category of the transformer.
        """
        self.name = name
        self.communication_protocol = communication_protocol
        self.transformer_type = transformer_type
        self.primary_voltage: float = 0.0
        self.secondary_voltage: float = 0.0
        self.tap_position: int = 0
        self.taps: List[int] = []


    def set_primary_voltage(self, voltage: float) -> None:
        """
        Sets the primary voltage of the transformer.
        
        Args:
            voltage (float): The primary voltage to be set.
        """
        self.primary_voltage = voltage


    def get_primary_voltage(self) -> float:
        """
        Gets the current primary voltage of the transformer.
        
        Returns:
            float: The current primary voltage.
        """
        return self.primary_voltage


    def set_secondary_voltage(self, voltage: float) -> None:
        """
        Sets the secondary voltage of the transformer.
        
        Args:
            voltage (float): The secondary voltage to be set.
        """
        self.secondary_voltage = voltage


    def get_secondary_voltage(self) -> float:
        """
        Gets the current secondary voltage of the transformer.
        
        Returns:
            float: The current secondary voltage.
        """
        return self.secondary_voltage


    def set_tap(self, position: int) -> None:
        """
        Sets the tap position of the transformer.
        
        Args:
            position (int): The tap position to be set.
        """
        if 0 <= position < len(self.taps):
            self.tap_position = position
        else:
            print("Invalid tap position. Tap position remains unchanged.")


    def get_tap(self) -> int:
        """
        Gets the current tap position of the transformer.
        
        Returns:
            int: The current tap position.
        """
        return self.tap_position


    def set_taps(self, num_taps: int) -> None:
        """
        Sets the number of taps available for the transformer.
        
        Args:
            num_taps (int): The number of taps to be set.
        """
        self.taps = list(range(num_taps))


    def get_taps(self) -> List[int]:
        """
        Gets the list of available tap positions for the transformer.
        
        Returns:
            List[int]: The list of tap positions.
        """
        return self.taps


    def set_state(self, primary_voltage: float, secondary_voltage: float, tap: int, num_taps: int) -> None:
        """
        Sets the complete state of the transformer, including primary voltage, secondary voltage, tap position, and number of taps.
        
        Args:
            primary_voltage (float): The primary voltage to be set.
            secondary_voltage (float): The secondary voltage to be set.
            tap (int): The tap position to be set.
            num_taps (int): The number of taps to be set.
        """
        self.set_primary_voltage(primary_voltage)
        self.set_secondary_voltage(secondary_voltage)
        self.set_tap(tap)
        self.set_taps(num_taps)


    def get_transformer_type(self) -> str:
        """
        Gets the type or category of the transformer.
        
        Returns:
            str: The transformer type.
        """
        return self.transformer_type


    def get_turns_ratio(self) -> int:
        """
        Gets the turns ratio of the transformer based on the current tap position.
        
        Returns:
            int: The turns ratio.
        """
        return self.taps[self.tap_position]


    def get_output_voltage(self) -> float:
        """
        Calculates and gets the output voltage of the transformer based on the primary voltage and turns ratio.
        
        Returns:
            float: The calculated output voltage.
        """
        return self.primary_voltage * self.get_turns_ratio()


    def adjust_voltage(self, adjustment: int) -> None:
        """
        Adjusts the tap position and, consequently, the secondary voltage of the transformer.
        
        Args:
            adjustment (int): The amount by which to adjust the tap position.
        """
        new_tap_position = self.tap_position + adjustment
        if 0 <= new_tap_position < len(self.taps):
            self.tap_position = new_tap_position
            self.secondary_voltage = self.primary_voltage * self.get_turns_ratio()
        else:
            print("Voltage adjustment not possible. Tap position remains unchanged.")