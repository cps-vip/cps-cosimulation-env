from dnp3.devices.master import Master

class StationMaster(Master):
    def __init__(self, name: str, master_dnp3_addr: int):
        super().__init__(name, master_dnp3_addr)

