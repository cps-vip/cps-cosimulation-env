from dnp3.dnp3_outstation import DNP3Outstation

class ProcessDevice(Device):
    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str):
        super().__init__(name, outstation, master_addr, socket_addr)