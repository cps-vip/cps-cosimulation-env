# Project documentation

device_modeling/
│
├── documentation/
│   ├── requirements.txt                  # List of project dependencies
│   └── README.md                         # Project documentation
│
├── simulations/
│   ├── helics-config.json                # Configuration file for HELICS co-simulation
│   ├── gridlab-d-config.glm              # Configuration file for GridLAB-D co-simulation
│   ├── run_simulation.py                 # Python script to execute the co-simulation
│   └── results/                          # Directory to store simulation results
│
├── src/
│   ├── process_level/                    # Layer 1: Process Level components
│   │   ├── relay_house.py                # For the Relay House
│   │   ├── protection_relays.py          # For Protection Relays
│   │   ├── voltage_current_sensors.py    # For Voltage and Current Sensors
│   │   ├── communication_interfaces.py   # For Communication Interfaces
│   │   │── sensors/                      # Directory for Sensors (CTs and VTs)
│   │   │   ├── current_transformers.py   # For Current Transformers (CTs)
│   │   │   └── voltage_transformers.py   # For Voltage Transformers (VTs)
│   │   └── ...
│   ├── bay_level/                        # Layer 2: Bay Level components
│   │   ├── bay_controllers.py            # For Bay Controllers
│   │   ├── switchgear.py                 # For Switchgear components
│   │   ├── circuit_breakers.py           # For Circuit Breakers
│   │   └── ...
│   ├── station_level/                    # Layer 3: Station Level components
│   │   ├── station_gateway.py            # For the Station Gateway
│   │   ├── human_machine_interface.py    # For Human-Machine Interface (HMI)
│   │   └── ...
│   ├── common/                           # Common components shared across layers
│   │   ├── modbus_interface.py           # For Modbus communication
│   │   ├── dnp3_interface.py             # For DNP3 communication
│   │   ├── iec61850_interface.py         # For IEC 61850 communication
│   │   └── ...
│   └── main.py                           # Main Python script to orchestrate the simulation
│
├── tests/
│   ├── unit_tests/                       # Directory for unit tests
│   ├── integration_tests/                # Directory for integration tests
│   └── formal_verification/              # Directory for formal verification tests
│
└── data/                                 # Directory for storing data or configuration files