#!/bin/bash
rm -rf *.png
rm -rf *.pov*
rm -rf *.inc*

python NeuroML2POVRay.py BigCerebellum.nml -split

mv BigCerebellum.pov BigCerebellum_s.pov
povray Antialias=On BigCerebellum_s.pov

B_PNG_S=BigCerebellum_s.png

python NeuroML2POVRay.py BigCerebellum.nml

povray Antialias=On BigCerebellum.pov

B_PNG_S=BigCerebellum.png


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
