from device_base.device import Device

class BayDevice(Device):
    def __init__(self, name: str, protocol: str, bay_name: str):
        super().__init__(name, protocol)
        self.bay_name = bay_name

    def get_bay_name(self) -> str:
        return self.bay_name