from src.process_level.sensors import Sensor

class CurrentTransformerSensor(Sensor):
    def __init__(self, name: str, protocol: str, ratio: float):
        super().__init__(name, protocol, sensor_type="Current Transformer")
        self.ratio = ratio

    def get_ratio(self) -> float:
        return self.ratio