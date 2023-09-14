(helics_broker -t="zmq" --federates=3 --name=mainbroker &> ./results/broker.log &)
cd Transmission
(exec python Transmission_simulator.py &> ../results/TransmissionSim.log &)
cd ..
cd Distribution
(gridlabd IEEE_123_feeder_0.glm &> ../results/DistributionSim.log &)
cd ..
cd Relay 
(exec python Relay_simulator.py)
cd ..
