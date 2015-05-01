NeuroMLToPOV-Ray
----------------

Converting NeuroML v1.8.1 and v2.0 files to POV-Ray: http://www.povray.org

**Still in development! Use with caution!**

This uses a Python (minidom) based parser which generates POVRay files directly for NeruoML v1.8.1 models ([NeuroML1ToPOVRay.py](https://github.com/NeuroML/NeuroMLToPOV-Ray/blob/master/NeuroML1ToPOVRay.py)).

It uses [libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) for NeuroML v2 models ([NeuroML2ToPOVRay.py](https://github.com/NeuroML/NeuroMLToPOV-Ray/blob/master/NeuroML2ToPOVRay.py)).

To get a feel for the usage of this tool, install POVRay (http://www.povray.org) and try running:

    ./test.sh
    
or (after installing libNeuroML)

    ./testv2.sh
    
This library has been used to generated some movies in 3D of NeuroML networks, e.g. [here](http://figshare.com/articles/NeuroML_models_in_3D/695845).

[![NeuroML network in 3D](http://previews.figshare.com/1051067/250_1051067.png)](http://figshare.com/articles/NeuroML_models_in_3D/695845).


