from src.process_level.process_device import ProcessDevice

class CircuitBreaker(ProcessDevice):
    def __init__(self, name: str, communication_protocol: str, max_current_rating: float):
        super().__init__(name, communication_protocol)
        self.max_current_rating = max_current_rating
        self.is_closed = False

    def close(self):
        pass

    def open(self):
        pass

    def get_max_current_rating(self) -> float:
        pass

    def is_circuit_closed(self) -> bool:
        pass