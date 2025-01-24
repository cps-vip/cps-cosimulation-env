import logging
import helics as h 

from process_level.circuit_breakers import CircuitBreaker
from process_level.protection_relays import ProtectionRelay
from process_level.transformers.distribution_transformer import DistributionTransformer
from bay_level.bay_controllers import BayController


# Config logger for use in all files
logging.basicConfig(filename="simulation.log", level=logging.INFO)
logger = logging.getLogger(__name__)

# Log messages at different levels
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")

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


def run_simulation(fed, transformer, protection_relay, circuit_breaker, bay_controller):
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
            voltage_monitoring_and_control(bay_controller, transformer)

        # Substation Response
        elif 22 * 3600 + 35 * 60 <= current_time < 23 * 3600:  # 22:35 to 23:00
            substation_response(transformer)

        # Simulated Fault Injection
        elif current_time == 24 * 3600:  # 00:00 next day
            simulated_fault_injection(protection_relay)

        # Fault Response
        elif current_time == 25 * 3600:  # 01:00 next day
            fault_response(protection_relay, circuit_breaker)

        # Fault Recovery
        elif current_time == 26 * 3600 + 1800:  # 01:00 to 02:30 next day
            fault_recovery(transformer, bay_controller)

        current_time += time_increment

    logger.info("Co-simulation completed.")


def sudden_load_increase(transformer):
    load_increase = 0.2
    new_primary_voltage = transformer.get_primary_voltage() * (1 - load_increase)
    transformer.set_primary_voltage(new_primary_voltage)
    logger.info("Sudden Load Increase: Voltage dropped due to load increase.")


def voltage_monitoring_and_control(bay_controller, transformer):
    target_voltage = 120.0
    current_voltage = transformer.get_output_voltage()

    if current_voltage < target_voltage:
        adjust_main_transformer_tap_settings(transformer)
        bay_controller.record_transformer_settings(transformer)
        bay_controller.record_voltage_data(current_voltage)

    logger.info("Voltage Monitoring and Control: Bay voltage regulation in progress.")


def adjust_main_transformer_tap_settings(transformer):
    # Implement Modbus communication to adjust tap settings
    pass


def substation_response(transformer):
    # Implement gradual return to normal voltage using Modbus commands
    pass


def simulated_fault_injection(protection_relay):
    protection_relay.trip()
    # Send fault information using DNP3 protocol


def fault_response(protection_relay, circuit_breaker):
    protection_relay.reset()
    circuit_breaker.open()
    # Send fault response information using DNP3 protocol

def fault_recovery(transformer, bay_controller):
    # TODO
    pass


if __name__ == "__main__":
    master_dnp3_address = 1

    broker = create_broker()
    # TODO: setup federate
    # fed, endpoint_bc, endpoint_mt, endpoint_pr, endpoint_cb = setup_federate()

    transformer = DistributionTransformer(name="MainTransformer", capacity=100.0)
    circuit_breaker = CircuitBreaker("CB1", 1024, master_dnp3_address, "127.0.0.1:20000", max_current=200.0)
    bay_controller = BayController("Bay1", 1025, master_dnp3_address, "127.0.0.1:20001")
    protection_relay = ProtectionRelay("Relay1", 1026, master_dnp3_address, "127.0.0.1:20002", relay_type="Overcurrent", current_rating=100.0, voltage_rating=120.0)

    run_simulation(None, transformer, protection_relay, circuit_breaker, bay_controller)
