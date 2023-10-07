from src.process_level.sensors import Sensor

class VoltageTransformerSensor(Sensor):
    def __init__(self, name: str, communication_protocol: str, ratio: float):
        super().__init__(name, communication_protocol, sensor_type="Voltage Transformer")
        self.ratio = ratio

    def get_ratio(self) -> float:
        return self.ratio