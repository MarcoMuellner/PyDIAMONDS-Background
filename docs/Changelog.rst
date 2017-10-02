#########
Changelog
#########

******
v1.1.0
******

Features
========

Background
----------

+   Provides properties for most datapoints created by DIAMONDS. This will be further expanded in 1.1.1 when pyDIAMONDS
    provides the methods necessary for the rest of the methods
+   The namespace was changed (background -> pyDiamondsBackground
+   Provided some strings (this will be further expanded)

Models
------

+   Standard & WhiteNoiseOscillationModel are now available as a a default implementation
+   Changed some names of the models

Testing
-------

+   The whole code is now completely tested when pushing

Misc
----

+ Added github pages and further documentation (This will also be further expanded)

******
v1.0.0
******

Features
========

Background
----------

+ Provides a simple class that acts as a wrapper to perform Background fitting.
+ Sets up DIAMONDS with the object it needs for a Nested Sampling run

Models
------

+ Provides an interface class from which custom models can be implemented.
+ Provides a simple model for noise only fitting

Testing
-------

+ Unittests are fully implemented for all methods of the Background class
+ Includes operational acceptance testing

Misc
----

+ A simple example is now available