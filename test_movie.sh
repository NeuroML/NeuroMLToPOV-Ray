#!/bin/bash
python NeuroML2POVRay.py  -movie -frames 72  -scalex 2 -scalez 2 BigCerebellum.nml
povray BigCerebellum_movie.ini
