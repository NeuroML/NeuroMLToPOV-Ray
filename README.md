NeuroMLToPOV-Ray
----------------

Converting NeuroML v1.8.1 (and eventually v2.0) files to POV-Ray: http://www.povray.org

**Still in development!! Use with caution!**

This version uses Python (minidom) based parser which generates POVRay files directly.

An improvement would be to use a SAX based parser.

**NOTE: doesn't (yet) use libNeuroML as there is a need to support NeuroML v1&2 (libNeuroML is currently only for v2)** 

To get a feel for the usage of this tool, install POVRay (http://www.povray.org) and try running:

    ./test.sh
    
This library has been used to generated some movies in 3D of NeuroML networks, e.g. [here](http://figshare.com/articles/NeuroML_models_in_3D/695845).

[![NeruoML network in 3D](http://previews.figshare.com/1051067/250_1051067.png)](http://figshare.com/articles/NeuroML_models_in_3D/695845).


