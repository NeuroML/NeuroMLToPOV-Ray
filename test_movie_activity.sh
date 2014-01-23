#!/bin/bash

cd SimulationData


### Generate POVRay files (split between cells & network) from NeuroML
python ../NeuroML2POVRay.py -split -scalex 3 -scalez 3  -background "<0,0,0,0.55>" MyNetwork.nml1


### Read in simulation as used in MyNetwork.nml1 & generate new POVRay files for each frame, coloured with cell activity
python ../OverlaySimulation.py MyNetwork -skip 20 -maxV 40 -minV -70 -rotations 1 


### Execute bash script to run povray on each frame file
chmod +x MyNetwork_pov.sh
./MyNetwork_pov.sh


cd -

