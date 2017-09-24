import numpy as np

class Background:
    def __init__(self,model,data,resultsPath,backgroundHyperParameters,nyquistFrequency,
                 xMeansConfiguratingParameters = None,nsmConfiguringParameters = None):
        self.backgroundModel = model
        self.data = data
        self._resultsPath = resultsPath
        self.backgroundHyperParameters = backgroundHyperParameters
        self._nyquistFrequency = nyquistFrequency

        if xMeansConfiguratingParameters is not None:
            self._xMeansConfigurating =xMeansConfiguratingParameters
        else:
            self._xMeansConfigurating = self.xMeansDefault()


        if nsmConfiguringParameters is not None:
            self._nsmConfiguringParameters = nsmConfiguringParameters
        else:
            self._nsmConfiguringParameters = self.nsmcDefault()

    @property
    def backgroundModel(self):
        return self._backgroundModel

    @backgroundModel.setter
    def backgroundModel(self,model):
        self._backgroundModel = model

    @property
    def backgroundHyperParameters(self):
        return self._backgroundHyperParameters

    @backgroundHyperParameters.setter
    def backgroundHyperParameters(self,parameters):
        self._backgroundHyperParameters = parameters

    def xMeansDefault(self):
        pass

    def nsmcDefault(self):
        pass

