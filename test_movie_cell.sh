#!/bin/bash

cd SimulationDataCell


### Generate POVRay files (split between cells & network) from NeuroML
python ../NeuroML2POVRay.py MyCellNet.nml1 -split -scalex 2 -scalez 1.2  -background "<0,0,0,0.55>" 


### Read in simulation as used in MyNetwork.nml1 & generate new povray files for each frame, coloured with cell segment activity
python ../ReadSim.py MyCellNet -singlecell -skip 10 -maxTime 100 -maxV 40 -minV -90 -rotations 0.5


### Execute bash script to run povray on each frame file
chmod +x MyCellNet_pov.sh
./MyCellNet_pov.sh


cd -
