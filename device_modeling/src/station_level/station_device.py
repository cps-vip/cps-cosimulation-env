from dnp3.devices.device import Device

class StationDevice(Device):
    def __init__(self, name: str):
        super().__init__(name)
