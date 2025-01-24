from process_level.process_device import ProcessDevice
        
class ProtectionRelay(ProcessDevice):
    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str, relay_type: str, current_rating: float, voltage_rating: float):
        super().__init__(name, outstation_addr, master_addr, socket_addr)
        self.relay_type = relay_type
        self.current_rating = current_rating
        self.voltage_rating = voltage_rating

    def trip(self):
        """
        Simulate the behavior of the protection relay tripping. Implement the logic for tripping the relay based on conditions.
        """
        # Implement the logic here to trip the relay when necessary
        self.status = "Tripped"

    def reset(self):
        """
        Reset the protection relay after tripping. Implement the logic to reset the relay to its normal state.
        """
        # Implement the logic here to reset the relay
        self.status = "Active"
