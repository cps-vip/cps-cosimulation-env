class switchGear():

    def __init__(self, name, protocol, voltage_rating, current_rating, switchgear_type):
        self.name = name
        self.protocol = protocol
        self.voltage_rating = voltage_rating # in kilovolts
        self.current_rating = current_rating # in amps
        self.switchgear_type = switchgear_type #metal-clad, metal-enclosed
        self.status = "OFF"
        self.is_tripped = False
    
    def turn_on(self):
        if self.status == "OFF" and self.is_tripped == False:
            self.status = "ON"
            print(self.name + " is now turned on.")
        elif self.status == "ON" and self.is_tripped == False:
            print(self.name + " is already on.")
        elif self.status == "OFF" and self.is_tripped == True:
            print(self.name + " is tripped!")
        else:
            print(self.name + "Something has gone horribly worng") #add else statements


    def turn_off(self):
        if self.status == "ON" and self.is_tripped == False:
            self.status = "OFF"
            print(self.name + " is now turned off.")
        elif self.status == "OFF" and self.is_tripped == False:
            print(self.name + " is already off.")
        elif self.status == "ON" and self.is_tripped == True:
            print(self.name + " is tripped!")

    def trip(self):
        if self.status == "ON" and self.is_tripped == False:
            self.is_tripped = True
            self.status = "OFF"
            print(self.name + " is tripped and there is a fault.")
        elif self.is_tripped == True:
            print(self.name + " is already been tripped.")
        elif self.status == "OFF":
            print(self.name + " is off, so it can't be tripped.")

    def reset(self):
        if self.is_tripped:
            self.is_tripped = False
            self.status = False
            print(self.name + " has been reset.")
        else:
            print("No need to reset. Has not been tripped.")

    def get_status(self):
        if self.is_tripped == True:
            print(self.name + " is currently " + self.status + " and is tripped.")
        else:
            print(self.name + " is currently " + self.status + " and is not tripped.")

    def __str__(self):
        if self.is_tripped == True:
            return self.name + " has the protocol " + self.protocol + ", has a voltage rating of " + str(self.voltage_rating) + ", has a current rating of " + str(self.current_rating) + ", is of the type " + self.switchgear_type + ", has a status of " + self.status + " and is tripped."
        else:
            return self.name + " has the protocol " + self.protocol + ", has a voltage rating of " + str(self.voltage_rating) + ", has a current rating of " + str(self.current_rating) + ", is of the type " + self.switchgear_type + ", has a status of " + self.status + " and is tripped."
    
    
