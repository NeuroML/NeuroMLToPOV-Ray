#!/bin/bash
cd SimulationDataCell
python ../NeuroML2POVRayMF.py MyCellNet.nml1 -split
python ../ReadSim_singleCell.py MyCellNet
chmod +x MyCellNet_pov.sh
./MyCellNet_pov.sh
cd -
