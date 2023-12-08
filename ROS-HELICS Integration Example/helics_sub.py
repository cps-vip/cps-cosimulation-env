import helics as h

fedinitstring = "--federates=2"
deltat = 0.01
helicsversion = h.helicsGetVersion()
print("HELICS version = " + str(helicsversion))
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreName(fedinfo, "Test Federate")
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
h.helicsFederateInfoSetCoreInitString(fedinfo, fedinitstring)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, deltat)

# Create value federate
fed = h.helicsCreateValueFederate("Test Federate", fedinfo)
print("Federate created")

# Register the subscription 
sub = h.helicsFederateRegisterSubscription(fed, "datacomm", "String")
print("Subscription registered")

# Enter execution mode
####----------------------------------------------------------------------------->> code seems to fail at this point
print("Before entering execution mode")
# h.helicsFederateEnterInitializingMode(fed)
print("Intialized")
# try:
#     status = h.helicsFederateEnterExecutingMode(fed)
# except Exception as e: 
#     print("Execute mode failed")
# print("After entering execution mode")

# This federate will only be subscribing to values
for t in range(1, 10):
    # current_time = h.helicsFederateRequestTime(fed, t * deltat)
    value = h.helicsInputGetString(sub)
    print(f"Time:, Received value: {value}")

h.helicsFederateFinalize(fed)
print("Federation finalized")

h.helicsFederateFree(fed)
h.helicsCloseLibrary()
print("Federate finalized")
