from src.process_level.sensors import Sensor

class CurrentTransformerSensor(Sensor):
    def __init__(self, name: str, ratio: float):
        super().__init__(name, sensor_type="Current Transformer")
        self.ratio = ratio

    def get_ratio(self) -> float:
        return self.ratio
