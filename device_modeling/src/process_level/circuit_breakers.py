from process_level.process_device import ProcessDevice


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
        self.position  = 0     # 0 for open, 1 for closed
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