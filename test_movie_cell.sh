#!/bin/bash
cd SimulationDataCell
python ../NeuroML2POVRay.py MyCellNet.nml1 -split -scalex 1.2 -scalez 1.2  -background "<0,0,0,0.55>" 
python ../ReadSim.py MyCellNet -singlecell -skip 10 -maxTime 100 -maxV 40 -minV -90
chmod +x MyCellNet_pov.sh
./MyCellNet_pov.sh
cd -
