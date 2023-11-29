from process_device import ProcessDevice
from protection_relays import ProtectionRelay
import time
import random
from uuid import uuid4

class RelayHouse(ProcessDevice):
    def __init__(self, name: str, communication_protocol: str, relays = {}):
        super().__init__(name, communication_protocol)
        self.relays = relays

    def set_relays(self, relays):
        self.relays = { i.name: i for i in relays }
    
    def get_relay(self, names):
        return [i for i in self.relays[name] if i in names]
    
    def add_relay(self, relay):
        self.relays[relay.name] = (relay)
    
    def remove_relay(self, relay_names):
        self.relays = { i.name: i for i in relays if i not in relay_names }

    def monitor_system(self, timestep, voltage, current):
        time.sleep(timestep)
        statusMap = {
            "Tripped": [],
            "Active": []
        }
        for relay in self.relay.values():
            if (voltage > relay.voltage_rating):
                relay.trip()
            if (current > relay.current_rating):
                relay.trip()
            statusMap[self.status].append(relay)
        yield statusMap
    
    def reset(self):
        for relay in self.relay.values():
            relay.reset()


if (__name__ == "__main__"):
    house = RelayHouse("house name", "commname")

    voltage = 10
    current = 10
    relayCount = 10

    house.set_relays([ProtectionRelay(str(uuid4()), "placeholder", i, i) for i in range(relayCount)])
    for out in house.monitor_system(1, voltage, current):
        voltage = random.randint(0, 10)
        voltage = random.randint(0, 10)
        print(out)
