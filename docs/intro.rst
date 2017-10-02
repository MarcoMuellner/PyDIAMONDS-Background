Introduction
============
PyDIAMONDS-Background is an extension to the Python bindings of the DIAMONDS code, which is available at
https://github.com/muma7490/PyDIAMONDS . It provides a simple interface, with which the user is able to fit signal,
providing a model that describes it. The package depends on ``numpy`` and ``pyDiamonds``.

Be sure to checkout the PyDIAMONDS code, as further documentation is provided there.

First example
-------------
A simple example.py of the background extension would look like this:

.. code-block:: python

    from pyDiamondsBackground import Background
    from pyDiamondsBackground.models import WhiteNoiseOnlyModel

    bg = Background(kicID='123456789',modelObject=WhiteNoiseOnlyModel,rootPath="exampleFiles")
    bg.run()
    bg.writeResults("exampleFiles/results/KIC123456789/run","background_")

This example expects the following file structure::

    -rootPath/
        -example.py
        -exampleFiles/
            -data/
                -KIC123456789.txt
            -results/
                -KIC123456789/
                    -run/
                    -background_hyperParameters_noise.txt
                    -NyquistFrequency.txt

Line by line explanation
------------------------
At the start, import necessary packages:

.. code-block:: python

    from pyDiamondsBackground import Background
    from pyDiamondsBackground.models import WhiteNoiseOnlyModel

Next you need to setup the nested sampler:

.. code-block:: python

    bg = Background(kicID='123456789',model=WhiteNoiseOnlyModel,rootPath="exampleFiles")

These three parameters are the simplest way to setup the Background class:

+   ``kicID``: This parameter defines the name of the object. It will be used to find the dataFile (in this case dataFile KIC*kicID*.txt) as well as the subfolder below results KIC*kicID*.
+   ``model``: This parameter defines the model which is used by DIAMONDS. This can be one of the default models provided by the package, or a custom model, which has to be derived from ``models.BackgroundModel``
+   ``rootPath``: This is the path where Background will look for the necessary files to create the internal objects.
        +   You don't necessarily have to set this path, but if you don't, you need to provide the rest of the optional
            parameters (see section about optional parameters). If you only set the optional parameters partially, you
            need to set this parameter (for which parameters are totally optional, see below). In general, parameters
            that are not set will be read through files, parameters that are set will not be read through files.

After the object is created, you can call run:

.. code-block:: python

    bg.run()

This will start the process of fitting the data. After the data is fitted, you can write the results to file. This is
only possible, if ``rootPath`` is set:

.. code-block:: python

    bg.writeResults("exampleFiles/results/KIC123456789/run","background")

The first parameter of writeResults defines the folder where the data is written, the second parameter defines a prefix
to the the fileNames.

This example shows how to work with the Background code provided you want to use files. There is also the possibility of
directly setting all parameters through the constructor.

File descriptions
-----------------

The Background code can handle a couple of different files. These have to fulfill the requirements of existing within
different subfolders, which have to be contained in the ``rootPath``. In the folder ``rootPath/data/`` you can have the
following files:

*   ``KIC$kicID$.txt``: This is the datafile on which the Background code will work. It has to be 2-dimensional, where
    the first column defines the x-Axis, the second defines the y-Axis

In the folder ``rootPath/results/`` you can have the following files:

*   ``KIC$kicID$/background_hyperParamters_$name$.txt``: This file defines the uniform priors used for the fitting.
    Their dimension is checked within the code and has to be equal the length set inside the model. The $name$ is also
    defined by the model.
*   ``KIC$kicID$/NyquistFrequency.txt``: This file defines the Nyquist frequency for the dataset.
*   ``KIC$kicID$/NSMC_configuringParameters.txt``: This file contains the configuring parameters for the Nested sampler
    used within Background. In general, you don't need to create this file or set the parameters via the constructor,
    default values are provided within Background.
*   ``KIC$kicID$/Xmeans_configuringParameters.txt``: This file contains the configuring parameters for the
    KmeansClusterer. In general, you don't need to create this file or set the parameters via the constructor,
    default values are provided within Background.

Other parameters
----------------

Background provides also the possibility to set other parameters directly through the constructor. These are
``data`` (the dataset), ``priors`` (the uniform priors) and ``nyquistFrequency`` (the nyquist frequency). If you set
these you don't need to set the root path (see examples folder for an example).






