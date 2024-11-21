from process_level.circuit_breakers import CircuitBreaker
from time import sleep
from random import randint

if __name__ == "__main__":
    master_dnp3_address = 1
    outstation_name = "testOutstation"
    outstation_dnp3_address = 1024
    outstation_ip = "127.0.0.1:20000"


    cb = CircuitBreaker(outstation_name, outstation_dnp3_address, master_dnp3_address, outstation_ip, 20)

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