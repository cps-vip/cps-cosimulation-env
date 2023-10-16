from src.device_base.device import Device

class ProcessDevice(Device):
    def __init__(self, name: str, communication_protocol: str):
        super().__init__(name, communication_protocol)