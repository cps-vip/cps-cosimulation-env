from dnp3.dnp3_outstation import DNP3Outstation

class ProcessDevice(DNP3Outstation):
    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str):
        super().__init__(name, outstation_addr, master_addr, socket_addr)
        self.device_name = name

    def get_device_name(self) -> str:
        return self.device_name
