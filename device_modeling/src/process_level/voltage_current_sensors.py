from src.process_level.process_device import ProcessDevice

class VoltageCurrentSensor(ProcessDevice):
    def __init__(self, voltage=0, current=0):
        self.voltage = voltage
        self.current = current

    def measure_voltage(self, voltage_reading):
        self.voltage = voltage_reading

    def measure_current(self, current_reading):
        self.current = current_reading

    def get_voltage(self):
        return self.voltage

    def get_current(self):
        return self.current

    def print_sensor_data(self):
        print(f"Voltage: {self.voltage} V, Current: {self.current} A")
