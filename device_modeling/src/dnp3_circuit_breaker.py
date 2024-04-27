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

	first_controller = MyOutStationNew()
	print('first_sensor instantiated')
	second_controller = MyOutStationNew()
	print('second_sensor instantiated')

	first_controller.start()
	print('first_sensor out_station started')
	second_controller.start()
	print('second_sensor outstation started')

	while cb1.is_closed:
		sleep(2)
		sensed_current = random.randint(int(cb1.get_max_current()) - 50, int(cb1.get_max_current()) + 10)
		print(f'sensing current of {sensed_current} on first index')
		first_controller.apply_update(opendnp3.Analog(value=float(sensed_current)), 0)
		sensed_current = random.randint(sensed_current - 2, sensed_current + 2)
		print(f'sensing current of {sensed_current} on second index')
		second_controller.apply_update(opendnp3.Analog(value=float(sensed_current)), 1)
		dnp3_value_first = cb1.master_station.get_val_by_group_variation_index(32, 1, 0)
		dnp3_value_second = cb1.master_station.get_val_by_group_variation_index(32, 1, 1)

		print(f'current is {dnp3_value_first}')
		if dnp3_value_first > cb1.get_max_current():
			cb1.open()
		print(f'current is {dnp3_value_second}')
		if dnp3_value_second > cb1.get_max_current():
			cb1.open()

	cb1.master_station.shutdown()
	print(f'{cb1.get_device_name()} master_station shutdown')

	first_controller.shutdown()
	print('some_controller out_station shutdown')

if __name__ == '__main__':
	main()
