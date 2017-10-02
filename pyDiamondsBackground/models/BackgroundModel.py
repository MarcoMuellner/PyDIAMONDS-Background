from pyDiamonds import Model
import numpy as np

class BackgroundModel(Model):
    def __init__(self, covariates, dimension, name, fileAppendix=""):
        covariates = covariates.astype(float)
        Model.__init__(self,covariates)
        self._dimension = dimension
        self._name = name
        self._fileAppendix = fileAppendix
        self._nyquistFrequency = None
        pass

    def getResponseFunction(self):
        return self._responseFunction

    def getNyquistFrequency(self):
        return self._nyquistFrequency

    def readNyquistFrequencyFromFile(self,fileName):
        self._nyquistFrequency = np.loadtxt(fileName).T

    @property
    def nyquistFrequency(self):
        if self._nyquistFrequency is None:
            raise ValueError("Nyquist frequency must be set before accessing it!")
        return self._nyquistFrequency

    @nyquistFrequency.setter
    def nyquistFrequency(self,value):
        self._nyquistFrequency = value
        self._calculateResponseFunction()

    def predict(self,predictions,modelParameters):
        raise NotImplementedError("You need to implement predict if you derive from BackgroundModel")

    @property
    def dimension(self):
        return self._dimension

    @property
    def name(self):
        return self._name

    @property
    def fileAppendix(self):
        return self._fileAppendix

    def _calculateResponseFunction(self):
        try:
            sincFunctionArgument = np.pi * self._covariates / (2 * self._nyquistFrequency)
            self._responseFunction = (np.sin(sincFunctionArgument) / sincFunctionArgument) ** 2
        except:
            raise ValueError("Nyquist frequency was not set before calculating response Function. Set the Nyquist "
                             "frequency before performing analysis")