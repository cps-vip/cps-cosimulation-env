from time import sleep
from random import randint

from process_level.circuit_breakers import CircuitBreaker
from process_level.transformers.distribution_transformer import DistributionTransformer
from bay_level.bay_controllers import BayController
from process_level.protection_relays import ProtectionRelay

if __name__ == "__main__":
    master_dnp3_address = 1
    outstation_name = "testOutstation"
    outstation_dnp3_address = 1024
    outstation_ip = "127.0.0.1:20000"


    cb = CircuitBreaker(outstation_name, outstation_dnp3_address, master_dnp3_address, outstation_ip, 20)


    transformer = DistributionTransformer(name="MainTransformer", capacity=100.0)
    circuit_breaker = CircuitBreaker("CB1", 1024, master_dnp3_address, "127.0.0.1:20000", max_current=200.0)
    bay_controller = BayController("Controller1", 1025, master_dnp3_address, "127.0.0.1:20001", "Bay 1")
    protection_relay = ProtectionRelay("Relay1", 1026, master_dnp3_address, "127.0.0.1:20002", relay_type="Overcurrent", current_rating=100.0, voltage_rating=120.0)


    cb.activate()
    sleep(1)
    trip_counter = 0
    current = 0
    while trip_counter < 2:
        current = randint(1, 30)
        if current > cb.get_max_current():
            cb.open()
            sleep(1)
            cb.close()
            trip_counter += 1
        sleep(1)
