#!/bin/bash
cd SimulationDataCell
python ../NeuroML2POVRay.py MyCellNet.nml1 -split -scalex 1.5 -scalez 1.5  -background "<0,0,0,0.55>" 
python ../ReadSim.py MyCellNet -singlecell
chmod +x MyCellNet_pov.sh
./MyCellNet_pov.sh
cd -
