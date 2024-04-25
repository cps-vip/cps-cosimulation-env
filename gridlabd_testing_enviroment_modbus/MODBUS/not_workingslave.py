import minimalmodbus
import time

slave = minimalmodbus.Instrument('/dev/ttys006', 1)  # Change 'COMy' to your virtual port
slave.serial.baudrate = 9600
slave.serial.bytesize = 8
slave.serial.parity = minimalmodbus.serial.PARITY_NONE
slave.serial.stopbits = 1
slave.serial.timeout = 1
slave.mode = minimalmodbus.MODE_RTU

REGISTER_ADDRESS = 100
while True:
    try:
        value = slave.read_register(REGISTER_ADDRESS)
        print(f"Received value: {value}")
        # slave.write_register(REGISTER_ADDRESS, value + 1)
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
