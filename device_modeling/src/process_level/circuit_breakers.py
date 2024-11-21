import time
from src.process_level.process_device import ProcessDevice
import helics as h
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def create_broker():
    initstring = "--federates=3 --name=mainbroker"
    broker = h.helicsCreateBroker("zmq", "", initstring)
    isconnected = h.helicsBrokerIsConnected(broker)

    if isconnected == 1:
        pass

    return broker

def destroy_federate(fed):
    h.helicsFederateDisconnect(fed)

    #    status, state = h.helicsFederateGetState(fed)
    #    assert state == 3

    while h.helicsBrokerIsConnected(broker):
        time.sleep(1)

    h.helicsFederateFree(fed)
    h.helicsCloseLibrary()

class CircuitBreaker(ProcessDevice):

    def __init__(self, name: str, protocol: str, max_current: float):
        """
        Constructor for the CircuitBreaker class.

        Initializes the object with a name, communication protocol, and maximum current rating.
        Also sets the initial state of the circuit breaker, indicating that it is closed, its position, and trip command.

        Args:
            name (str): The name of the circuit breaker.
            protocol (str): The communication protocol used.
            max_current (float): The maximum current rating of the circuit breaker.
        """
        super().__init__(name, protocol)
        self.max_current = max_current
        self.is_closed = True  # Circuit breaker is initially closed
        self.position  = 1     # 0 for open, 1 for closed
        self.trip_cmd  = False


    def close(self):
        """
        Method to close the circuit breaker.

        Checks if the circuit breaker is already closed; if not, it sets it to a closed state, updates its position, and resets the trip command.
        Prints a message indicating that the circuit breaker is now closed.
        """
        try:
            if not self.is_closed:
                self.is_closed = True
                self.position  = 1
                self.trip_cmd  = False
                print(f"{self.name} circuit breaker is now closed.")
            else:
                print(f"{self.name} circuit breaker is already closed.")
        except Exception as e:
            print(f"An error occurred while closing the circuit breaker: {e}")


    def open(self):
        """
        Method to open the circuit breaker.

        Checks if the circuit breaker is already open; if not, it sets it to an open state, updates its position, and resets the trip command.
        Prints a message indicating that the circuit breaker is now open.
        """
        try:
            if self.is_closed:
                self.is_closed = False
                self.position = 0
                self.trip_cmd = False
                print(f"{self.name} circuit breaker is now open.")
            else:
                print(f"{self.name} circuit breaker is already open.")
        except Exception as e:
            print(f"An error occurred while opening the circuit breaker: {e}")


    def get_max_current(self) -> float:
        """
        Method to get the maximum current rating of the circuit breaker.

        Returns:
            float: The maximum current rating of the circuit breaker.
        """
        return self.max_current


    def is_closed_status(self) -> bool:
        """
        Method to check whether the circuit breaker is currently closed or not.

        Returns:
            bool: True if the circuit breaker is closed, False if it is open.
        """
        return self.is_closed


    def trip(self):
        """
        Method to issue a trip command for the circuit breaker.

        Checks if a trip command has already been issued; if not, it sets the trip command to True
        and prints a message indicating that the trip command has been issued.
        """
        try:
            if not self.trip_cmd:
                self.trip_cmd = True
                self.open()
                print(f"Trip command issued for {self.name} circuit breaker.")
            else:
                print(f"Trip command has already been issued for {self.name} circuit breaker.")
        except Exception as e:
            print(f"An error occurred while issuing the trip command: {e}")


    # IEC 61850 specific methods and attributes:
    def get_node_name(self) -> str:
        """
        Method to get a logical node name associated with the circuit breaker.

        Returns:
            str: The logical node name associated with the circuit breaker.
        """
        return f"CBR:{self.name}"


    def get_status_data(self) -> dict:
        """
        Method to get a dictionary containing simulated status information related to the circuit breaker.

        This includes the "Oper" status (indicating whether the circuit breaker is open or closed) and the position ("Pos") of the circuit breaker.

        Returns:
            dict: A dictionary containing status information.
        """
        try:
            return {
                "Oper": self.is_closed,
                "Pos": str(self.position)
            }
        except Exception as e:
            print(f"An error occurred while getting status data: {e}")

if __name__ == "__main__":
    cb = CircuitBreaker(name="CB1", protocol="Protocol1", max_current=200.0)
    #################################  Registering  federate from json  ########################################
    fed = h.helicsCreateValueFederateFromConfig("circuit_breakers_config.json")
    h.helicsFederateRegisterInterfaces(fed, "circuit_breakers_config.json")
    federate_name = h.helicsFederateGetName(fed)
    logger.info("HELICS Version: {}".format(h.helicsGetVersion()))
    logger.info("{}: Federate {} has been registered".format(federate_name, federate_name))
    pubkeys_count = h.helicsFederateGetPublicationCount(fed)
    subkeys_count = h.helicsFederateGetInputCount(fed)
    ######################   Reference to Publications and Subscription form index  #############################
    pubid = {}
    subid = {}
    for i in range(0, pubkeys_count):
        pubid["m{}".format(i)] = h.helicsFederateGetPublicationByIndex(fed, i)
        pubtype = h.helicsPublicationGetType(pubid["m{}".format(i)])
        pubname = h.helicsPublicationGetName(pubid["m{}".format(i)])
        logger.info("{}: Registered Publication ---> {}".format(federate_name, pubname))
    for i in range(0, subkeys_count):
        subid["m{}".format(i)] = h.helicsFederateGetInputByIndex(fed, i)
        h.helicsInputSetDefaultComplex(subid["m{}".format(i)], 0, 0)
        sub_key = h.helicsSubscriptionGetTarget(subid["m{}".format(i)])
        logger.info("{}: Registered Subscription ---> {}".format(federate_name, sub_key))

    ######################   Entering Execution Mode  ##########################################################
    h.helicsFederateEnterInitializingMode(fed)
    status = h.helicsFederateEnterExecutingMode(fed)
    # Pypower Processing (inputs)
    hours = 10
    total_inteval = int(60 * 60 * hours)
    grantedtime = -1
    pf_interval    = 5 * 60  # in seconds (minimim_resolution) ## Adjust this to change PF intervals

    for t in range(0, total_inteval, pf_interval):

        while grantedtime < t:
            grantedtime = h.helicsFederateRequestTime(fed, t)

        #############################   Subscribing to Feeder Load from to GridLAB-D ##############################################
        for i in range(0, subkeys_count):
            sub = subid["m{}".format(i)]
            demand = h.helicsInputGetComplex(sub)
            rload = demand.real
            iload = demand.imag

        if (not cb.is_closed_status()):
            rload = 0
            iload = 0

        ############################   Publishing Voltage to GridLAB-D #######################################################
        for i in range(0, pubkeys_count):
            pub = pubid["m{}".format(i)]
            status = h.helicsPublicationPublishComplex(pub, rload, iload)
        # status = h.helicsEndpointSendEventRaw(epid, "fixed_price", 10, t)

        logger.info("{}: Federate Granted Time = {}".format(federate_name,grantedtime))
        logger.info("{}: Substation Load from Distribution System = {} kW".format(federate_name, complex(round(rload,2), round(iload,2)) / 1000))

        if ((t > 20000) and cb.is_closed_status()):
            cb.trip()


    ##############################   Terminating Federate   ########################################################
    t = 60 * 60 * 10
    while grantedtime < t:
        grantedtime = h.helicsFederateRequestTime(fed, t)
    logger.info("{}: Destroying federate".format(federate_name))
    destroy_federate(fed)
    logger.info("{}: Done!".format(federate_name))
