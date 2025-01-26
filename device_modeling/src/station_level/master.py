import os
from ctypes import CDLL, c_char_p, c_uint16
from .station_device import StationDevice
from device_base.device import DeviceState
from dnp3.config_classes import RuntimePtr, MasterChannelPtr, MasterChannelConfig

libmasterpath = os.path.abspath(os.path.join(os.path.dirname(__file__), r'../../build/libmaster.so'))
libmaster = CDLL(libmasterpath)

# TODO - 
# init
# destroy
# activate
# deactivate
class DNP3Master(StationDevice):
    def __init__(self, name: str, master_dnp3_addr: int, outstation_dnp3_addr:int, outstation_ip: str):
        super().__init__(name)
        self.master_dnp3_addr = master_dnp3_addr
        self.outstation_dnp3_addr = outstation_dnp3_addr
        self.outstation_ip = outstation_ip

        init_runtime = libmaster.init_runtime
        init_runtime.restype = RuntimePtr
        self._runtime = init_runtime()
        if self._runtime.value is None:
                raise Exception()

        create_master_channel_config = libmaster.create_master_channel_config
        create_master_channel_config.argtypes = [c_uint16]
        create_master_channel_config.restype = MasterChannelConfig
        self.config = create_master_channel_config(master_dnp3_addr)

        create_tcp_channel = libmaster.create_tcp_channel
        create_tcp_channel.argtypes = [RuntimePtr, c_uint16, c_char_p]
        create_tcp_channel.restype = MasterChannelPtr
        self._master_channel = create_tcp_channel(self._runtime, master_dnp3_addr, outstation_ip.encode())

        self.state = DeviceState.INITIALIZED
    # Implement abstract method in Device base class
    def destroy(self) -> None:
        if self._runtime is not None:
            destroy_runtime = libmaster.destroy_runtime
            destroy_runtime.argtypes = [RuntimePtr]
            destroy_runtime.restype = None
            destroy_runtime(self._runtime)
        if self._master_channel is not None:
            destroy_master_channel = libmaster.destroy_master_channel
            destroy_master_channel.argtypes = [MasterChannelPtr]
            destroy_master_channel.restype = None
            destroy_master_channel(self._master_channel)
    # Implement abstract method in Device base class
    def activate(self) -> None:
        if self.state == DeviceState.INITIALIZED:
            self.state = DeviceState.ACTIVE
        elif self.state == DeviceState.INACTIVE:
            # Outstation was deactivated, just need to start it up again
            if self._master_channel is None:
                raise Exception("Master was never initialized. Did you accidentally set the device state manually?")
            enable_master_channel = libmaster.enable_master_channel
            enable_master_channel.argtypes = [MasterChannelPtr]
            enable_master_channel.restype = None
            enable_master_channel(self._master_channel)
            self.state = DeviceState.ACTIVE
        else:
            raise Exception("Cannot activate Master from state")
    # Implement abstract method in Device base class
    def deactivate(self) -> None:
        if self.state != DeviceState.ACTIVE:
            raise Exception("Trying to deactivate master from bad state")
        if self._master_channel is None:
            raise Exception("Master was never initialized. Did you accidentally set the device state manually?")
        disable_master_channel = libmaster.disable_master_channel
        disable_master_channel.argtypes = [MasterChannelPtr]
        disable_master_channel.restype = None
        disable_master_channel(self._master_channel)
        self.state = DeviceState.INACTIVE

    def run(self):
        run_channel = libmaster.run_channel
        run_channel.argtypes = [MasterChannelPtr, c_uint16]
        run_channel.restype = c_uint16
        if run_channel(self._master_channel, self.outstation_dnp3_addr) == -1:
            raise Exception()
        
