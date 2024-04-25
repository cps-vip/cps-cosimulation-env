from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import struct

# Subclass ModbusSlaveContext to add functionality to print values on read/write
class PrintingModbusSlaveContext(ModbusSlaveContext):
    # This will be runned anyways, thats why we intersept it (Thats the normal way to do it)
    def getValues(self, fx, address, count=1):
        values = super(PrintingModbusSlaveContext, self).getValues(fx, address, count)
        # print(f"Read Values: Function Code: {fx}, Address: {address}, Values: {values}")
        # for i in range(len(values)):
        #     print(f"Read Values: Value{i}: {values[i]}")
        # return values

    def setValues(self, fx, address, values):
        super(PrintingModbusSlaveContext, self).setValues(fx, address, values)
        # For debugging perpuses
        # print(f"Write Values: Function Code: {fx}, Address: {address}, Values: {values}")
        packed_voltage_real = struct.pack('>HH', values[0], values[1])
        packed_voltage_imag = struct.pack('>HH', values[2], values[3])

        voltage_real = struct.unpack('>f', packed_voltage_real)[0]
        voltage_imag = struct.unpack('>f', packed_voltage_imag)[0]

        if voltage_imag >= 0:
            print(f"Read Values: ({voltage_real} + {voltage_imag}j) V")
        else:
            print(f"Read Values: ({voltage_real} - {voltage_imag}j) V")

        return values

# Initialize each type of data block appropriately
di_data_block = ModbusSequentialDataBlock(0, [0]*100)  # Discrete Inputs: OFF state
co_data_block = ModbusSequentialDataBlock(0, [0]*100)  # Coils: OFF state
hr_data_block = ModbusSequentialDataBlock(0, [0]*100)  # Holding Registers: Zero-initialized
ir_data_block = ModbusSequentialDataBlock(0, [0]*100)  # Input Registers: Zero-initialize

# Create a datastore and populate it with some registers
store = PrintingModbusSlaveContext(
    di=di_data_block,
    co=co_data_block,
    hr=hr_data_block,
    ir=ir_data_block)

context = ModbusServerContext(slaves=store, single=True)

# Set the server identity
identity = ModbusDeviceIdentification()
identity.VendorName = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = ''
identity.ProductName = 'pymodbus Server'
identity.ModelName = 'pymodbus Server'
identity.MajorMinorRevision = '2.3.0'

# Run the server with the correct keyword arguments
StartTcpServer(context=context, identity=identity, address=("localhost", 502))
