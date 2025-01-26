from station_level.master import DNP3Master
from time import sleep

if __name__ == "__main__":
    master_name = "testMaster"
    master_dnp3_address = 1
    outstation_dnp3_address = 1024
    outstation_ip = "127.0.0.1:20000"


    master = DNP3Master(master_name, master_dnp3_address, outstation_dnp3_address, outstation_ip)

    master.activate()
    master.run()
    sleep(30)