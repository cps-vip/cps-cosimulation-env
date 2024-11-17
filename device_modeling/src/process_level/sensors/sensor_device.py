from src.process_level.process_device import ProcessDevice

class Sensor(ProcessDevice):
    def __init__(self, name: str, sensor_type: str):
        super().__init__(name)
        self.sensor_type = sensor_type

    def get_sensor_type(self) -> str:
        return self.sensor_type
