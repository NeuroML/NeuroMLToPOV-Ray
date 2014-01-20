#!/bin/bash
cd SimulationData
python ../NeuroML2POVRay.py -split -scalex 3 -scalez 3  -background "<0,0,0,0.55>" MyNetwork.nml1
python ../ReadSim.py MyNetwork
chmod +x MyNetwork_pov.sh
./MyNetwork_pov.sh
cd -
