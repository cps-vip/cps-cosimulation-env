import minimalmodbus
import time

master = minimalmodbus.Instrument('/dev/ttys007', 1)  # Change 'COMx' to your virtual port
master.serial.baudrate = 9600
master.serial.bytesize = 8
master.serial.parity = minimalmodbus.serial.PARITY_NONE
master.serial.stopbits = 1
master.serial.timeout = 1
master.mode = minimalmodbus.MODE_RTU

REGISTER_ADDRESS = 100
while True:
    try:
        value = 12345  # Any test value
        master.write_register(REGISTER_ADDRESS, value)
        # read_value = master.read_register(REGISTER_ADDRESS)
        print(f"Sent value: {value}, Read back:") #{read_value}")
        time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")