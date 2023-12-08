#!/bin/bash

mkdir -p results/
TIMESTAMP=$(date +%s)

BROKER_LOG="./results/broker_$TIMESTAMP.log"
TRANSMISSION_LOG="./results/TransmissionSim_$TIMESTAMP.log"
DISTRIBUTION_LOG="./results/DistributionSim_$TIMESTAMP.log"

touch $BROKER_LOG
touch $TRANSMISSION_LOG
touch $DISTRIBUTION_LOG

HELICS_BROKER=`which helics_broker`
($HELICS_BROKER -t="zmq" --federates=3 --name=mainbroker > $BROKER_LOG)&

cd Transmission
python Transmission_simulator.py > ../$TRANSMISSION_LOG 2>&1 &
cd ..

cd Distribution
gridlabd IEEE_123_feeder_0.glm > ../$DISTRIBUTION_LOG 2>&1 &
cd ..

cd Relay 
(exec python Relay_simulator.py)
cd ..
