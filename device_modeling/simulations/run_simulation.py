import helics as h
import time
import logging
from bay_level.bay_controllers import BayController
from process_level.circuit_breakers import CircuitBreaker
from process_level.protection_relays import ProtectionRelay

from process_level.transformers.transformer_device import Transformer


# Create a logger instance
logger = logging.getLogger(__name__)

# Add a StreamHandler to send log messages to the console
logger.addHandler(logging.StreamHandler())

# Set the logger level to DEBUG to capture messages at and above this level
logger.setLevel(logging.DEBUG)

# Log messages at different levels
logger.debug("This is a debug message")
#logger.info("This is an info message")
#logger.warning("This is a warning message")
#logger.error("This is an error message")
#logger.critical("This is a critical message")


def create_broker():
    """
    This function is responsible for creating and connecting to a HELICS broker.

    Returns:
        broker: HELICS broker object.
    """
    initstring = "--federates=4 --name=mainbroker"
    broker = h.helicsCreateBroker("zmq", "", initstring) # https://docs.helics.org/en/main/user-guide/advanced_topics/CoreTypes.html
    isconnected = h.helicsBrokerIsConnected(broker)

    if isconnected == 1:
        pass

    return broker


def destroy_federate(fed):
    """
    This function is responsible for disconnecting and freeing a HELICS federate.

    Args:
        fed: HELICS federate object.
    """
    h.helicsFederateDisconnect(fed)
    h.helicsFederateFree(fed)
    h.helicsCloseLibrary()


def setup_federate():
    """
    Set up and register the HELICS federate.

    Returns:
        fed: HELICS federate object.
    """
    pass


def run_simulation(fed, transformer, protection_relay, circuit_breaker, bay_controller,
                   endpoint_bay_controller, endpoint_main_transformer, endpoint_protection_relay, endpoint_circuit_breaker):
    start_time = 22 * 3600        # 22:00 in seconds
    end_time   = (24 + 4) * 3600  # 04:00 next day in seconds

    current_time = start_time
    time_increment = 300  # 5 minutes in seconds

    while current_time <= end_time:
        logger.info(f"Current Simulation Time: {current_time}")

        # Sudden Load Increase
        if current_time == 22 * 3600 + 30 * 60:  # 22:30
            sudden_load_increase(transformer)

        # Voltage Monitoring and Control
        elif 22 * 3600 + 30 * 60 <= current_time < 22 * 3600 + 35 * 60:  # 22:30 to 22:35
            voltage_monitoring_and_control(bay_controller, transformer, endpoint_main_transformer)

        # Substation Response
        elif 22 * 3600 + 35 * 60 <= current_time < 23 * 3600:  # 22:35 to 23:00
            substation_response(transformer, endpoint_main_transformer)

        # Simulated Fault Injection
        elif current_time == 24 * 3600:  # 00:00 next day
            simulated_fault_injection(protection_relay, endpoint_protection_relay)

        # Fault Response
        elif current_time == 25 * 3600:  # 01:00 next day
            fault_response(protection_relay, circuit_breaker, endpoint_circuit_breaker)

        # Fault Recovery
        elif current_time == 26 * 3600 + 1800:  # 01:00 to 02:30 next day
            fault_recovery(transformer, bay_controller, endpoint_main_transformer)

        current_time += time_increment

    logger.info("Co-simulation completed.")


def sudden_load_increase(transformer):
    load_increase = 0.2
    new_primary_voltage = transformer.get_primary_voltage() * (1 - load_increase)
    transformer.set_primary_voltage(new_primary_voltage)
    logger.info("Sudden Load Increase: Voltage dropped due to load increase.")


def voltage_monitoring_and_control(bay_controller, transformer, endpoint_main_transformer):
    target_voltage = 120.0
    current_voltage = transformer.get_output_voltage()

    if current_voltage < target_voltage:
        adjust_main_transformer_tap_settings(transformer, endpoint_main_transformer)
        bay_controller.record_transformer_settings(transformer)
        bay_controller.record_voltage_data(current_voltage)

    logger.info("Voltage Monitoring and Control: Bay voltage regulation in progress.")


def adjust_main_transformer_tap_settings(transformer, endpoint_main_transformer):
    # Implement Modbus communication to adjust tap settings
    # Example: h.helicsEndpointSendBytesTo(endpoint_main_transformer, "ModbusCommand", command_data)
    pass


def substation_response(transformer, endpoint_main_transformer):
    # Implement gradual return to normal voltage using Modbus commands
    # Example: h.helicsEndpointSendBytesTo(endpoint_main_transformer, "ModbusCommand", command_data)
    pass


def simulated_fault_injection(protection_relay, endpoint_protection_relay):
    protection_relay.trip()
    # Send fault information using DNP3 protocol


def fault_response(protection_relay, circuit_breaker, endpoint_circuit_breaker):
    protection_relay.reset()
    circuit_breaker.open()
    # Send fault response information using DNP3 protocol


def fault_recovery(transformer, bay_controller, endpoint_main_transformer):


if __name__ == "__main__":
    broker = create_broker()
    fed, endpoint_bc, endpoint_mt, endpoint_pr, endpoint_cb = setup_federate()

    transformer      = Transformer(name="MainTransformer", communication_protocol="Modbus", transformer_type="Distribution")
    protection_relay = ProtectionRelay(name="Relay1", relay_type="Overcurrent", current_rating=100.0, voltage_rating=120.0, communication_protocol="DNP3")
    circuit_breaker  = CircuitBreaker(name="CB1", protocol="IEC61850", max_current=200.0)
    bay_controller   = BayController(name="Bay1")

    bay_controller.add_device(transformer)
    bay_controller.add_device(protection_relay)
    bay_controller.add_device(circuit_breaker)

    run_simulation(fed, transformer, protection_relay, circuit_breaker, bay_controller, endpoint_bc, endpoint_mt, endpoint_pr, endpoint_cb)