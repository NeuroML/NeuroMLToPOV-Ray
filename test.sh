#!/bin/bash

### Cleanup

./clean.sh


### Generate a single POVRay file from NeuroML & use povray to generate PNG from this

python NeuroML1ToPOVRay.py BigCerebellum.nml

povray Antialias=On BigCerebellum.pov

B_PNG=BigCerebellum.png


### Generate POVRay files (split between cells & network) from NeuroML & use povray to generate PNG from these

python NeuroML1ToPOVRay.py BigCerebellum.nml -split

mv BigCerebellum.pov BigCerebellum_s.pov
povray Antialias=On BigCerebellum_s.pov

B_PNG_S=BigCerebellum_s.png


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
