class sensorDevice:
    def __init__(self, sensor_id, name, unit):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.value = None

    def read_value(self):
        #Reading sensor value (from hardware, etc) ???
        raise NotImplementedError("This method needs to be overridden in the subclass")

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return f"Sensor {self.name} (ID: {self.sensor_id}) - {self.value} {self.unit}"
#snake case for file name, camel case for class name