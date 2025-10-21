from dnp3.devices.outstation import Outstation

class ProcessDevice(Outstation):
    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str):
        super().__init__(name, outstation_addr, master_addr, socket_addr)
