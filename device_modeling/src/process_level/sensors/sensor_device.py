from src.process_level.process_device import ProcessDevice

class Sensor(ProcessDevice):
    def __init__(self, name: str, communication_protocol: str, sensor_type: str):
        super().__init__(name, communication_protocol)
        self.sensor_type = sensor_type

    def get_sensor_type(self) -> str:
        return self.sensor_type
