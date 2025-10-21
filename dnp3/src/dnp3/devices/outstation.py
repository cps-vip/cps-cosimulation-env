from .device import Device, DeviceState

from dnp3 import tcpserver, outstation

class Outstation(Device):
    class TCPServer:
        def __init__(self, socket_addr: str):
            self._runtime = tcpserver.init_runtime()
            self._server = tcpserver.init_server(self._runtime, socket_addr)

        def start(self):
            tcpserver.start_server(self._server)

        def destroy(self):
            tcpserver.destroy_runtime(self._runtime)

    def __init__(self, name: str, outstation_addr: int, master_addr: int, socket_addr: str):
        # Make sure to initialize the Device base class
        super().__init__(name)

        self._outstation_addr = outstation_addr
        self._master_addr = master_addr
        self._socket_addr = socket_addr

        # One time intitializations belong in init

        # "any" can be replaced by IP addresses w/ wildcards; e.g., "192.168.0.*"
        self._address_filter = outstation.create_address_filter("any")
        self._config = outstation.create_outstation_config(self._outstation_addr, self._master_addr)
        self._tcpserver = self.TCPServer(self._socket_addr)

        # Not initialized in __init__, but good practice to show it will be used later
        self._outstation = None

        # This is the property in the Device base class
        self.state = DeviceState.INITIALIZED

    # Implement abstract method in Device base class
    def activate(self) -> None:
        """
        Associates the outstation to the given TCP server. Also initializes the database.
        """
        if self.state == DeviceState.INITIALIZED:
            # Bind the oustation to the TCP server
            self._outstation = outstation.add_outstation(self._tcpserver._server, self._address_filter, self._config)

            # Initialize outstation database
            outstation.init_database(self._outstation)

            # Start TCP server and change state
            self._tcpserver.start()
            self.state = DeviceState.ACTIVE
        elif self.state == DeviceState.INACTIVE:
            # Outstation was deactivated, just need to start it up again
            if self._outstation is None:
                raise Exception("Outstation was never initialized. Did you accidentally set the device state manually?")
            outstation.enable_outstation(self._outstation)
            self.state = DeviceState.ACTIVE
        else:
            raise Exception(f"Cannot activate outstation from state {self.state}")

    # Implement abstract method in Device base class
    def deactivate(self) -> None:
        if self.state != DeviceState.ACTIVE:
            raise Exception("Trying to deactivate outstation from bad state")

        if self._outstation is None:
            raise Exception("Outstation was never initialized. Did you accidentally set the device state manually?")
        outstation.disable_outstation(self._outstation)
        self.state = DeviceState.INACTIVE

    # Implement abstract method in Device base class
    def destroy(self) -> None:
        if self.state != DeviceState.INACTIVE:
            raise Exception("Trying to destroy master from bad state")
        self._tcpserver.destroy()
        self.state = DeviceState.DESTROYED

