from sensorDevice import sensorDevice

class current_transformer_sensor(sensorDevice):
    def __init__(self, sensor_id, name, unit, current_rating):
        super().__init__(sensor_id, name, unit)
        self.current_rating = current_rating

    def read_value(self):
        #Needs to be overriden in subclass based on actual sensor reading
        import random
        self.value = random.uniform(0, self.current_rating)
        return self.value

    def __str__(self):
        return f"Current Transformer Sensor {self.name} (ID: {self.sensor_id}) - {self.value} {self.unit}, Current Rating: {self.current_rating}A"