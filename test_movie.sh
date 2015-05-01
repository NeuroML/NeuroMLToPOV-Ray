#!/bin/bash

### Generate a PovRay ini file to generate a movie with 36 frames
python NeuroML1ToPOVRay.py  -movie -frames 36  -scalex 2 -scalez 2 BigCerebellum.nml


### Generate the movie using povray
povray BigCerebellum_movie.ini
