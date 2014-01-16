#!/bin/bash
cd SimulationData
python ../NeuroML2POVRay.py MyNetwork.nml1 -split
python ../ReadSim.py MyNetwork
chmod +x MyNetwork_pov.sh
./MyNetwork_pov.sh
cd -
