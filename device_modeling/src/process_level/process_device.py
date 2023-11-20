from device_base.device import Device

class ProcessDevice(Device):
    def __init__(self, name: str, protocol: str):
        super().__init__(name, protocol)