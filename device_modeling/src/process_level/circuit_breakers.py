from src.process_level.process_device import ProcessDevice

class CircuitBreaker(ProcessDevice):

    """
    This is the constructor method for the CircuitBreaker class. It initializes the object with a name, 
    communication protocol, and maximum current rating. It also sets the initial state of the circuit breaker, 
    indicating that it is closed, its position, and trip command.
    """
    def __init__(self, name: str, communication_protocol: str, max_current_rating: float):
        super().__init__(name, communication_protocol)
        self.max_current_rating = max_current_rating
        self.is_closed = True  # Circuit breaker is initially closed
        self.position = 0  # 0 for open, 1 for closed
        self.trip_command = False


    """
    This method is used to close the circuit breaker. It checks if the circuit breaker is already closed; 
    if not, it sets it to a closed state, updates its position, and resets the trip command. 
    It also prints a message indicating that the circuit breaker is now closed.
    """
    def close(self):
        try:
            if not self.is_closed:
                self.is_closed = True
                self.position = 1
                self.trip_command = False
                print(f"{self.name} circuit breaker is now closed.")
            else:
                print(f"{self.name} circuit breaker is already closed.")
        except Exception as e:
            print(f"An error occurred while closing the circuit breaker: {e}")


    """
    This method is used to open the circuit breaker. Similar to the close method, it checks if the circuit breaker 
    is already open; if not, it sets it to an open state, updates its position, and resets the trip command. 
    It prints a message indicating that the circuit breaker is now open.
    """
    def open(self):
        try:
            if self.is_closed:
                self.is_closed = False
                self.position = 0
                self.trip_command = False
                print(f"{self.name} circuit breaker is now open.")
            else:
                print(f"{self.name} circuit breaker is already open.")
        except Exception as e:
            print(f"An error occurred while opening the circuit breaker: {e}")


    """
    This method returns the maximum current rating of the circuit breaker.
    """
    def get_max_current_rating(self) -> float:
        return self.max_current_rating


    """
    This method returns a boolean value indicating whether the circuit breaker is currently closed or not.
    """
    def is_circuit_closed(self) -> bool:
        return self.is_closed


    """
    This method is used to issue a trip command for the circuit breaker. It checks if a trip command has already been issued;
      if not, it sets the trip command to True and prints a message indicating that the trip command has been issued.
    """
    def trip(self):
        try:
            if not self.trip_command:
                self.trip_command = True
                print(f"Trip command issued for {self.name} circuit breaker.")
            else:
                print(f"Trip command has already been issued for {self.name} circuit breaker.")
        except Exception as e:
            print(f"An error occurred while issuing the trip command: {e}")

    
    # IEC 61850 specific methods and attributes:

    """
    This method returns a logical node name associated with the circuit breaker, typically used in communication protocols within substations.
    """
    def get_logical_node_name(self) -> str:
        return f"CBR:{self.name}"

    """
    This method returns a dictionary containing simulated status information related to the circuit breaker. 
    This includes the "Oper" status (indicating whether the circuit breaker is open or closed) and the position ("Pos") of the circuit breaker.
    """
    def get_status_data(self) -> dict:
        try:
            return {
                "Oper": "false" if self.is_closed else "true",
                "Pos": str(self.position)
            }
        except Exception as e:
            print(f"An error occurred while getting status data: {e}")