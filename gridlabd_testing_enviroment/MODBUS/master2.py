from pymodbus.client import ModbusTcpClient
import time

# Initialize the client
client = ModbusTcpClient('localhost', port=5020)
client.connect()

# Function to write values to the server every second
def write_values():
    address = 0x00  # The address to write to
    value = 0       # Starting value
    while True:
        time.sleep(1)
        value += 1
        client.write_register(address, value)
        print(f"Written value: {value}")

write_values()
