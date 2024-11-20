import os

from ctypes import CDLL, c_char_p, c_uint16, c_int

from dnp3.config_classes import OutstationConfig, ServerPtr, AddressFilterPtr, OutstationPtr, RuntimePtr
from device_base.device import Device, DeviceState

# Have to supply absolute path if the shared library isn't in /usr/lib
liboutpath = os.path.abspath(os.path.join(os.path.dirname(__file__), r'../../build/liboutstation.so'))
libout = CDLL(liboutpath)

libtcppath = os.path.abspath(os.path.join(os.path.dirname(__file__), r'../../build/libtcpserver.so'))
libtcp = CDLL(libtcppath)


class DNP3Outstation(Device):
    # TODO: Change raise Exception() to something more useful everywhere it appears
    class TCPServer:
        def __init__(self, socket_addr: str):
            init_runtime = libtcp.init_runtime
            init_runtime.restype = RuntimePtr
            self._runtime = init_runtime()
            if self._runtime.value is None:
                raise Exception()

            init_server = libtcp.init_server
            init_server.argtypes = [RuntimePtr, c_char_p]
            init_server.restype = ServerPtr
            self._server = init_server(self._runtime, socket_addr.encode())
            if self._server.value is None:
                raise Exception()

        def destroy(self):
            if self._server is not None and self._server.value is not None:
                destroy_server = libtcp.destroy_server
                destroy_server.argtypes = [ServerPtr]
                destroy_server.restype = None
                destroy_server(self._server)

            if self._runtime is not None and self._runtime.value is not None:
                destroy_runtime = libtcp.destroy_runtime
                destroy_runtime.argtypes = [RuntimePtr]
                destroy_runtime.restype = None
                destroy_runtime(self._runtime)

        def start(self):
            start_server = libtcp.start_server
            start_server.argtypes = [ServerPtr]
            start_server.restype = c_int
            if start_server(self._server) == -1:
                raise Exception()


    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str):
        # Make sure to initialize the Device base class
        super().__init__(name)

        self._outstation_addr = outstation_addr
        self._master_addr = master_addr
        self._socket_addr = socket_addr

        # One time intitializations belong in init.
        create_address_filter = libout.create_address_filter
        create_address_filter.argtypes = [c_char_p]
        create_address_filter.restype = AddressFilterPtr
        self._address_filter = create_address_filter("any".encode())
        if self._address_filter.value is None:
            raise Exception()

        create_outstation_config = libout.create_outstation_config
        create_outstation_config.argtypes = [c_uint16, c_uint16]
        create_outstation_config.restype = OutstationConfig
        self._config = create_outstation_config(self._outstation_addr, self._master_addr)

        self._tcpserver = self.TCPServer(self._socket_addr)

        # This is the property in the Device base class
        self.state = DeviceState.INITIALIZED

    # Implement abstract method in Device base class
    def destroy(self) -> None:
        if self._address_filter is not None and self._address_filter.value is not None:
            destroy_address_filter = libout.destroy_address_filter
            destroy_address_filter.argtypes = [AddressFilterPtr]
            destroy_address_filter.restype = None
            destroy_address_filter(self._address_filter)

        if self._outstation is not None and self._outstation.value is not None:
            destroy_outstation = libout.destroy_outstation
            destroy_outstation.argtypes = [OutstationPtr]
            destroy_outstation.restype = None
            destroy_outstation(self._outstation)

        if self._tcpserver is not None:
            self._tcpserver.destroy()

        self.state = DeviceState.DESTROYED

    # Implement abstract method in Device base class
    def activate(self) -> None:
        """
        Associates the outstation to the given TCP server. Also initializes the database.
        """
        if self.state == DeviceState.INITIALIZED:
            # Bind the oustation to the TCP server
            add_outstation = libout.add_outstation
            add_outstation.argtypes = [ServerPtr, AddressFilterPtr, OutstationConfig]
            add_outstation.restype = OutstationPtr
            self._outstation = add_outstation(self._tcpserver._server, self._address_filter, self._config)
            if self._outstation.value is None:
                raise Exception()

            # Initialize outstation database
            init_database = libout.init_database
            init_database.argtypes = [OutstationPtr]
            init_database.restype = None
            init_database(self._outstation)

            # Start TCP server and change state
            self._tcpserver.start()
            self.state = DeviceState.ACTIVE
        elif self.state == DeviceState.INACTIVE:
            # Outstation was deactivated, just need to start it up again
            if self._outstation is None or self._outstation.value is None:
                raise Exception("Outstation was never initialized. Did you accidentally set the device state manually?")
            enable_outstation = libout.enable_outstation
            enable_outstation.argtypes = [OutstationPtr]
            enable_outstation.restype = None
            enable_outstation(self._outstation)
            self.state = DeviceState.ACTIVE
        else:
            raise Exception("Cannot activate outstation from state")

    # Implement abstract method in Device base class
    def deactivate(self) -> None:
        if self.state != DeviceState.ACTIVE:
            raise Exception("Trying to deactivate outstation from bad state")

        if self._outstation is None or self._outstation.value is None:
            raise Exception("Outstation was never initialized. Did you accidentally set the device state manually?")
        disable_outstation = libout.disable_outstation
        disable_outstation.argtypes = [OutstationPtr]
        disable_outstation.restype = None
        disable_outstation(self._outstation)
        self.state = DeviceState.INACTIVE

