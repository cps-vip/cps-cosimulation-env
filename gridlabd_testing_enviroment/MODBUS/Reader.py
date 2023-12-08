from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Subclass ModbusSlaveContext to add functionality to print values on read/write
class PrintingModbusSlaveContext(ModbusSlaveContext):
    def getValues(self, fx, address, count=1):
        values = super(PrintingModbusSlaveContext, self).getValues(fx, address, count)
        # print(f"Read Values: Function Code: {fx}, Address: {address}, Values: {values}")
        print(f"Read Values: {values}")
        return values

    # def setValues(self, fx, address, values):
    #     super(PrintingModbusSlaveContext, self).setValues(fx, address, values)
    #     print(f"Write Values: Function Code: {fx}, Address: {address}, Values: {values}")

# Create a datastore and populate it with some registers
store = PrintingModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),  # Discrete Inputs Initialization
    co=ModbusSequentialDataBlock(0, [17]*100),  # Coils Initialization
    hr=ModbusSequentialDataBlock(0, [17]*100),  # Holding Register Initialization
    ir=ModbusSequentialDataBlock(0, [17]*100))  # Input Registers Initialization

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
