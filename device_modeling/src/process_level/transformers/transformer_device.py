class Transformer:
    def __init__(self, name: str, communication_protocol: str, transformer_type: str):
        self.transformer_type = transformer_type
        self.primary_voltage = 0
        self.secondary_voltage = 0

    #Getters/Setters
    
    def set_primary_voltage(self, voltage):
        self.input_voltage = 0
    
    def get_primary_voltage(self, voltage):
        return self.input_voltage
    
    def set_secondary_voltage(self, voltage):
        self.output_voltage = 0
    
    def get_secondary_voltage(self, voltage):
        return self.output_voltage
    
    def set_state(self, primary_volatage, secondary_voltage):
        self.set_primary_voltage(primary_volatage)
        self.set_secondary_voltage(secondary_voltage)

    def get_transformer_type(self) -> str:
        return self.transformer_type
    
    def get_turns_ratio(self):
        return self.taps[self.tap_position]

    def get_output_voltage(self):
        return self.primary_voltage * self.get_turns_ratio()
    
    
    #Behavior
    def set_tap(self, position):
        if 0 <= position and position < len(self.taps):
            self.tap_position = position
        else:
            print("Invalid tap position. Tap position remains unchanged.")

    def adjust_voltage(self, adjustment):
        new_tap_position = self.tap_position + adjustment
        if 0 <= new_tap_position  and new_tap_position < len(self.taps):
            self.tap_position = new_tap_position
            self.output_voltage = self.primary_voltage * self.get_turns_ratio()
        else:
            print("Voltage adjustment not possible. Tap position remains unchanged.")

    
    