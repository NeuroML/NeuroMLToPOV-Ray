#!/bin/bash

### Cleanup

./clean.sh


### Generate a single POVRay file from NeuroML & use povray to generate PNG from this

python NeuroML2ToPOVRay.py NeuroML2/Ex6_CerebellumDemo.net.nml

povray Antialias=On NeuroML2/Ex6_CerebellumDemo.net.pov

B_PNG=NeuroML2/Ex6_CerebellumDemo.net.png


### Generate POVRay files (split between cells & network) from NeuroML & use povray to generate PNG from these

python NeuroML2ToPOVRay.py NeuroML2/Ex6_CerebellumDemo.net.nml -split

mv NeuroML2/Ex6_CerebellumDemo.net.pov NeuroML2/Ex6_CerebellumDemo.net_s.pov
povray Antialias=On NeuroML2/Ex6_CerebellumDemo.net_s.pov

B_PNG_S=NeuroML2/Ex6_CerebellumDemo.net_s.png


### Check images have been generated

if [ -s $B_PNG ] && [ -s $B_PNG_S ]; then
    echo "--------------------------"
    echo "    Success!!"
    echo "--------------------------"
    echo ""
else
    echo "--------------------------"
    echo "    Failure!!"
    echo "--------------------------"
    echo ""
fi
