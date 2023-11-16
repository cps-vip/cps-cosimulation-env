from src.process_level.process_device import ProcessDevice

class RelayHouse(ProcessDevice):
    def __init__(self, name: str, communication_protocol: str):
        super().__init__(name, communication_protocol)