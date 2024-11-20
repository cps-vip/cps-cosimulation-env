from station_level.station_device import StationDevice

# TODO - 
# init
# destroy
# activate
# deactivate
class DNP3Master(StationDevice):
    def __init__(self, name: str, dnp3_addr: int, outstation_ip: str):
        super().__init__(name)
        self.dnp3_addr = dnp3_addr
        self.outstation_ip = outstation_ip

    # Implement abstract method in Device base class
    def destroy(self) -> None:

    # Implement abstract method in Device base class
    def activate(self) -> None:
       
    # Implement abstract method in Device base class
    def deactivate(self) -> None:
        