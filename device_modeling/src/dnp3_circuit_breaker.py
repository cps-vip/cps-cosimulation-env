from process_level.circuit_breakers import CircuitBreaker
from dnp3_python.dnp3station.outstation_new import MyOutStationNew
from pydnp3 import opendnp3
import random
from time import sleep

def main():
    cb1 = CircuitBreaker('test_breaker_1', 'DNP3', 100)
    cb1.activate()

    print(f'{cb1.get_device_name()}  instantiated with max current {cb1.get_max_current()}')

    cb1.master_station.start()
    print(f'{cb1.get_device_name()} master_station started')

    some_controller = MyOutStationNew()
    print('some_sensor instantiated')

    some_controller.start()
    print('some_sensor out_station started')

    while cb1.is_closed:
        sleep(1)
        sensed_current = random.randint(int(cb1.get_max_current()) - 50, int(cb1.get_max_current()) + 10)
        print(f'testing current of {sensed_current}')
        some_controller.apply_update(opendnp3.Analog(value=float(sensed_current)), 0)
        dnp3_value = cb1.master_station.get_val_by_group_variation_index(30, 6, 0)
        print(f'current is {dnp3_value}')
        if dnp3_value > cb1.get_max_current():
            cb1.open()

    cb1.master_station.shutdown()
    print(f'{cb1.get_device_name()} master_station shutdown')

    some_controller.shutdown()
    print('some_controller out_station shutdown')

if __name__ == '__main__':
    main()
