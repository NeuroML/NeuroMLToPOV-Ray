#!/bin/bash
cd SimulationDataCell
python ../NeuroML2POVRay.py MyCellNet.nml1 -split
python ../ReadSim.py MyCellNet
chmod +x MyCellNet_pov.sh
./MyCellNet_pov.sh
cd -
