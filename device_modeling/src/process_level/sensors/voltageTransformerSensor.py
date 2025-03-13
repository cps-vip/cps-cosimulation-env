from sensorDevice import sensorDevice

class voltage_transformer_sensor(sensorDevice):
    def __init__(self, sensor_id, name, unit, voltage_rating):
        super().__init__(sensor_id, name, unit)
        self.voltage_rating = voltage_rating
        
    def read_value(self):
        #Needs to be overriden in subclass based on actual sensor reading
        import random
        self.value = random.uniform(0, self.voltage_rating)
        return self.value
    
    def __str__(self):
        return f"Voltage Transformer Sensor {self.name} (ID: {self.sensor_id}) - {self.value} {self.unit}, Voltage Rating: {self.voltage_rating}V"