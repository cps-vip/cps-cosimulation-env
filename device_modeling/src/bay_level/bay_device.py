from dnp3.devices.outstation import Outstation

class BayDevice(Outstation):
    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str, bay_name: str):
        super().__init__(name, outstation_addr, master_addr, socket_addr)
        self.bay_name = bay_name

    def get_bay_name(self) -> str:
        return self.bay_name
