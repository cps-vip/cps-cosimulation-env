(helics_broker -t="zmq" --federates=2 --name=mainbroker &> ./results/broker.log &)
cd Transmission
(exec python Transmission_simulator.py &> ../results/TransmissionSim.log &)
cd ..
cd Distribution
(gridlabd IEEE_123_feeder_0.glm &> ../results/DistributionSim.log &)
cd ..
