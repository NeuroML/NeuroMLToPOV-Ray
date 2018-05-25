NeuroMLToPOV-Ray
----------------

### Note: the latest version of this export to POV-Ray has been moved to [pyNeuroML](https://github.com/NeuroML/pyNeuroML). For exporting NML2 from NEURON use [this](https://github.com/NeuroML/pyNeuroML/blob/master/examples/export_neuroml2.py) and then use pynml-povray (see [here](https://github.com/NeuroML/pyNeuroML/blob/f65953414e391da9b1169c6a5d0e4883358c7094/test.sh#L87-L89)). See also [here](https://github.com/NeuroML/pyNeuroML/tree/master/pyneuroml/povray). 
### This repo can still be used for converting _NeuroML v1.8.1_ files to POV-Ray

-------------------------------

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


