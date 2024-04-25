# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 10:08:26 2018

@author: monish.mukherjee
"""
import scipy.io as spio
from pypower.api import case118, ppoption, runpf, runopf
import math
import numpy
import matplotlib.pyplot as plt
import time
import helics as h
import random
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def create_broker():
    initstring = "--federates=2 --name=mainbroker"
    broker = h.helicsCreateBroker("zmq", "", initstring)
    isconnected = h.helicsBrokerIsConnected(broker)

    if isconnected == 1:
        pass

    return broker



def destroy_federate(fed):
    h.helicsFederateDisconnect(fed)

    #    status, state = h.helicsFederateGetState(fed)
    #    assert state == 3

    #while h.helicsBrokerIsConnected(broker):
    #    time.sleep(1)

    h.helicsFederateFree(fed)
    h.helicsCloseLibrary()


if __name__ == "__main__":

    #broker = create_broker()
    # fed = create_federate()

    #################################  Registering  federate from json  ########################################

    fed = h.helicsCreateValueFederateFromConfig("Relay_config.json")
    h.helicsFederateRegisterInterfaces(fed, "Relay_config.json")
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
        sub_key = h.helicsInputGetTarget(subid["m{}".format(i)])
        logger.info("{}: Registered Subscription ---> {}".format(federate_name, sub_key))

    ######################   Entering Execution Mode  ##########################################################
    h.helicsFederateEnterInitializingMode(fed)
    status = h.helicsFederateEnterExecutingMode(fed)

    # Pypower Processing (inputs)
    hours = 24
    total_inteval = int(60 * 60 * hours)
    grantedtime = -1
    sensing_interval    = 5 * 60  # in seconds (minimim_resolution) ## Adjust this to change PF intervals
    random.seed(0)

    ###########################   Cosimulation Bus and Load Amplification Factor #########################################

    #########################################   Starting Co-simulation  ####################################################

    for t in range(0, total_inteval, sensing_interval):

        ############################   Subscribing to CurrentA from GridLAB-D #######################################################

        while grantedtime < t:
            grantedtime = h.helicsFederateRequestTime(fed, t)

        #############################   Subscribing to Feeder Load from to GridLAB-D ##############################################
        logger.info("{}: Federate Granted Time = {}".format(federate_name,grantedtime))
        for i in range(0, subkeys_count):
            sub = subid["m{}".format(i)]
            name = h.helicsInputGetTarget(sub) 
            current = h.helicsInputGetComplex(sub)
            logger.info("{}: Substation {} to Distribution System = {} A".format(federate_name, name, current))
        # print(voltage_plot,real_demand)

    ##########################   Creating headers and Printing results to CSVs #####################################

    ##############################   Terminating Federate   ########################################################
    t = 60 * 60 * 24
    while grantedtime < t:
        grantedtime = h.helicsFederateRequestTime(fed, t)
    logger.info("{}: Destroying federate".format(federate_name))
    destroy_federate(fed)
    logger.info("{}: Done!".format(federate_name))
