from src.station_level.station_device import StationDevice

# TODO - everything
class DNP3Master(StationDevice):
    def __init__(self, name: str, dnp3_addr: int, outstation_ip: str):
        super().__init__(name)
        self.dnp3_addr = dnp3_addr
        self.outstation_ip = outstation_ip

