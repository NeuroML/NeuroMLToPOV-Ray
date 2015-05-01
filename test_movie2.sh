#!/bin/bash

### Generate a PovRay ini file to generate a movie with 36 frames
python NeuroML2ToPOVRay.py  -movie -frames 36  -scalex 2 -scalez 2 NeuroML2/Ex6_CerebellumDemo.net.nml


### Generate the movie using povray
povray NeuroML2/Ex6_CerebellumDemo.net_movie.ini
