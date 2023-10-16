# python -m unittest -v tests/unit_tests/circuitbreaker_unit_test.py

from src.process_level.circuit_breakers import CircuitBreaker
import unittest

class TestCircuitBreaker(unittest.TestCase):

    def setUp(self):
        # Create a CircuitBreaker instance for testing
        self.circuit_breaker = CircuitBreaker(name="CB_Prototype", communication_protocol="IEC61850", max_current_rating=100.0)

    def test_close_circuit_breaker(self):
        self.circuit_breaker.open()   # Open it first
        self.circuit_breaker.close()  # Close it
        self.assertTrue(self.circuit_breaker.is_circuit_closed())
        self.assertEqual(self.circuit_breaker.position, 1)

    def test_open_circuit_breaker(self):
        self.circuit_breaker.close()  # Close it first
        self.circuit_breaker.open()   # Open it
        self.assertFalse(self.circuit_breaker.is_circuit_closed())
        self.assertEqual(self.circuit_breaker.position, 0)

    def test_trip_circuit_breaker(self):
        self.circuit_breaker.trip()  # Issue a trip command
        self.assertTrue(self.circuit_breaker.trip_command)

    def test_get_max_current_rating(self):
        max_current = self.circuit_breaker.get_max_current_rating()
        self.assertEqual(max_current, 100.0)

    def test_get_logical_node_name(self):
        logical_node_name = self.circuit_breaker.get_logical_node_name()
        self.assertEqual(logical_node_name, "CBR:CB_Prototype")

    def test_get_status_data(self):
        status_data = self.circuit_breaker.get_status_data()
        self.assertIsInstance(status_data, dict)
        self.assertIn("Oper", status_data)
        self.assertIn("Pos", status_data)

    def test_default_state(self):
        # Ensure the default state of the circuit breaker is closed
        self.assertTrue(self.circuit_breaker.is_circuit_closed())
        self.assertEqual(self.circuit_breaker.position, 1)
        self.assertFalse(self.circuit_breaker.trip_command)

if __name__ == '__main__':
    unittest.main()