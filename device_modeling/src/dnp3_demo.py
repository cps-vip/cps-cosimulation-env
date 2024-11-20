from dnp3.dnp3_outstation import DNP3Outstation
from station_level.master import DNP3Master

master_name = "testMaster"
master_dnp3_address = 1
oustation_name = "testOutstation"
outstation_dnp3_address = 1024
outstation_ip = "127.0.0.1:20000"


master = DNP3Master(master_name, master_dnp3_address, outstation_dnp3_address, outstation_ip)
outstation = DNP3Outstation(oustation_name, outstation_dnp3_address, master_dnp3_address, outstation_ip)

outstation.activate()
master.activate()
