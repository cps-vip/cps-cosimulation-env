from dnp3_python.dnp3station.outstation_new import MyOutStationNew
from dnp3_python.dnp3station.master_new import MyMasterNew
from pydnp3 import opendnp3
import random
from time import sleep

master = MyMasterNew()
out = MyOutStationNew()


def getConfig():
	print(f'Showcasing get_config() for master and out\n'
		  f'MASTER: {master.get_config()}\n'
		  f'OUT: {out.get_config()}\n')
def addOutstation(name: str, to_add: MyOutStationNew):
	print(f'Showcasing add_outstation_app')
	out.add_outstation_app('out2', to_add)
	sleep(2)
	print(f'{name} added to out\'s outstation pool')
def main():
	master.start()
	out.start()
	sleep(2)
	getConfig()
	addOutstation('out2', MyOutStationNew())
	print(out.get_outstation_app('out2').get_config())
	print(f'TODO: showcase more functions, particularly the master commands')

if __name__ == '__main__':
	main()