#!/bin/bash
# run from /device_modeling/src

mkdir -p results/
TIMESTAMP=$(date +%s)

MASTER_LOG="./results/Master_$TIMESTAMP.log"
OUTSTATION_LOG="./results/Outstation_$TIMESTAMP.log"

touch $MASTER_LOG
touch $OUTSTATION_LOG

python3 master_demo.py > $MASTER_LOG 2>&1 &

python3 outstation_demo.py > $OUTSTATION_LOG 2>&1 &

sleep 20s

pkill -9 python