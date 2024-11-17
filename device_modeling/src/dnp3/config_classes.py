from ctypes import c_void_p, c_int, c_uint16, Structure, c_bool, c_uint64, c_uint32

class OutstationFeatures(Structure):
    _fields_ = [("self_address", c_bool),
                ("broadcast", c_bool),
                ("unsolicited", c_bool),
                ("respond_to_any_master", c_bool)]

class ClassZeroConfig(Structure):
    _fields_ = [("binary", c_bool),
                ("double_bit_binary", c_bool),
                ("binary_output_status", c_bool),
                ("counter", c_bool),
                ("frozen_counter", c_bool),
                ("analog", c_bool),
                ("analog_output_status", c_bool),
                ("octet_string", c_bool)]

class DecodeLevel(Structure):
    # Note: these are actually enums. Look at the generated dnp3.h for definitions.
    _fields_ = [("application", c_int),
                ("transport", c_int),
                ("link", c_int),
                ("physical", c_int)]

class EventBufferConfig(Structure):
    _fields_ = [("max_binary", c_uint16),
                ("max_double_bit_binary", c_uint16),
                ("max_binary_output_status", c_uint16),
                ("max_counter", c_uint16),
                ("max_frozen_counter", c_uint16),
                ("max_analog", c_uint16),
                ("max_analog_output_status", c_uint16),
                ("max_octet_string", c_uint16)]

class OutstationConfig(Structure):
    _fields_ = [("outstation_address", c_uint16),
                ("master_address", c_uint16),
                ("event_buffer_config", EventBufferConfig),
                ("solicited_buffer_size", c_uint16),
                ("unsolicited_buffer_size", c_uint16),
                ("rx_buffer_size", c_uint16),
                ("decode_level", DecodeLevel),
                ("confirm_timeout", c_uint64),
                ("select_timeout", c_uint64),
                ("outstation_features", OutstationFeatures),
                ("max_unsolicited_retries", c_uint32),
                ("unsolicited_retry_delay", c_uint64),
                ("keep_alive_timeout", c_uint64),
                ("max_read_request_headers", c_uint16),
                ("max_controls_per_request", c_uint16),
                ("class_zero", ClassZeroConfig)]

class MasterChannelConfig(Structure):
    _fields_ = [("master_address", c_uint16),
                ("tx_buffer_size", c_uint16),
                ("rx_buffer_size", c_uint16),
                ("decode_level", DecodeLevel)]


class RuntimeConfig(Structure):
    _fields_ = [("num_core_threads", c_uint16)]

class RuntimePtr(c_void_p):
    pass

class OutstationPtr(c_void_p):
    pass

class AddressFilterPtr(c_void_p):
    pass

class MasterChannelPtr(c_void_p):
    pass

class ServerPtr(c_void_p):
    pass