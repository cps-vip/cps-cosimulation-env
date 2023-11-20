# Run under "device_modeling" folder: python3 src/circuit_breakers_demo.py

from process_level.circuit_breakers import CircuitBreaker  # Assuming your CircuitBreaker class is in a separate module named circuit_breaker

# Instantiate a CircuitBreaker
cb = CircuitBreaker(name="CB1", protocol="Protocol1", max_current=100.0)

# Perform operations that should comply with contracts
try:
    cb.close()
    cb.trip()
    cb.open()
    max_current = cb.get_max_current()
    is_closed = cb.is_closed_status()
    node_name = cb.get_node_name()
    status_data = cb.get_status_data()

    print("Operations completed successfully.")
except Exception as e:
    print(f"Contract violation: {e}")